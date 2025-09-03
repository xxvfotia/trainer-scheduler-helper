import argparse, csv
from collections import defaultdict

def to_minutes(t):
    h,m = map(int, t.split(':'))
    return h*60+m

def load_sessions(p):
    rows = list(csv.DictReader(open(p,encoding='utf-8')))
    for r in rows:
        r['start_m'] = to_minutes(r['start'])
        r['end_m'] = to_minutes(r['end'])
        r['dur'] = r['end_m']-r['start_m']
    return rows

def load_trainers(p):
    rows = list(csv.DictReader(open(p,encoding='utf-8')))
    by_day = defaultdict(list)
    for r in rows:
        r['start_m'] = to_minutes(r['start'])
        r['end_m'] = to_minutes(r['end'])
        r['max_daily_minutes'] = int(float(r['max_daily_hours'])*60)
        by_day[r['day']].append(r)
    return by_day

def assign(sessions, avail):
    out = []
    used_minutes = defaultdict(lambda: defaultdict(int)) # trainer->day->minutes
    order = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    for day in sorted(set(s['day'] for s in sessions), key=lambda d: order.index(d)):
        day_sess = [s for s in sessions if s['day']==day]
        day_sess.sort(key=lambda x: x['start_m'])
        for s in day_sess:
            candidates = []
            for tr in avail.get(day,[]):
                within_window = (s['start_m'] >= tr['start_m']) and (s['end_m'] <= tr['end_m'])
                has_capacity = used_minutes[tr['trainer']][day] + s['dur'] <= tr['max_daily_minutes']
                if within_window and has_capacity:
                    candidates.append(tr['trainer'])
            assigned = candidates[0] if candidates else ''
            out.append({
                'child': s['child'],
                'day': day,
                'start': s['start'],
                'end': s['end'],
                'location': s['location'],
                'trainer': assigned or 'UNASSIGNED'
            })
            if assigned:
                used_minutes[assigned][day] += s['dur']
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sessions', required=True)
    ap.add_argument('--trainers', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    sessions = load_sessions(args.sessions)
    avail = load_trainers(args.trainers)
    out = assign(sessions, avail)
    with open(args.out,'w',newline='',encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['child','day','start','end','location','trainer'])
        w.writeheader()
        w.writerows(out)
    print(f"Wrote {args.out}")

if __name__ == '__main__':
    main()
