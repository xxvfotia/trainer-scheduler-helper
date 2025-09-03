# Trainer Scheduler Helper (Hello Hoku)

Greedy assignment of trainers to sessions given **availability windows** and **daily capacity limits**. Outputs a **weekly schedule CSV** to reduce conflicts and gaps.

![Hello Hoku — schedule sample](https://github.com/xxvfotia/trainer-scheduler-helper/blob/main/schedule-sample.png?raw=true)


## Why this exists
Coordinating sessions by hand is slow and error-prone. This helper produces a reasonable first pass you can review, tweak, and share—without needing a full optimization stack.

## What it does
- Reads **sessions** and **trainer availability** from CSVs.
- Assigns each session to the **first available trainer** whose time window covers the session **and** who still has daily capacity.
- Writes `output/schedule.csv` with **UNASSIGNED** rows clearly visible when no trainer fits.

> Baseline by design: transparent, easy to edit, and safe to iterate in a real program.

---
