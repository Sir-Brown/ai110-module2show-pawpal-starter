# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule for D'Jaine (2026-10-28)
--------------------------------------------------
07:30  Morning walk  Mochi      30 min  [high]    [ ]
08:00  Feeding       Whiskers   10 min  [high]    [x]
09:00  Grooming      Mochi      20 min  [low]     [ ]
09:00  Medication    Whiskers    5 min  [high]    [ ]
15:30  Playtime      Whiskers   15 min  [low]     [ ]
18:00  Evening walk  Mochi      30 min  [medium]  [ ]
18:00  Training      Mochi      15 min  [medium]  [ ]

Conflict warnings
--------------------------------------------------
WARNING: Conflict on 2026-10-28 at 18:00: Evening walk (Mochi), Training (Mochi)
WARNING: Conflict on 2026-10-28 at 09:00: Grooming (Mochi), Medication (Whiskers)

Mochi's tasks
--------------------------------------------------
07:30  Morning walk  Mochi      30 min  [high]    [ ]
09:00  Grooming      Mochi      20 min  [low]     [ ]
18:00  Evening walk  Mochi      30 min  [medium]  [ ]
18:00  Training      Mochi      15 min  [medium]  [ ]

Incomplete tasks
--------------------------------------------------
07:30  Morning walk  Mochi      30 min  [high]    [ ]
08:00  Feeding       Whiskers   10 min  [high]    [ ]  due 2026-10-29
09:00  Grooming      Mochi      20 min  [low]     [ ]
09:00  Medication    Whiskers    5 min  [high]    [ ]
15:30  Playtime      Whiskers   15 min  [low]     [ ]
18:00  Evening walk  Mochi      30 min  [medium]  [ ]
18:00  Training      Mochi      15 min  [medium]  [ ]

Completed tasks
--------------------------------------------------
08:00  Feeding       Whiskers   10 min  [high]    [x]

Whiskers' incomplete tasks
--------------------------------------------------
08:00  Feeding       Whiskers   10 min  [high]    [ ]  due 2026-10-29
09:00  Medication    Whiskers    5 min  [high]    [ ]
15:30  Playtime      Whiskers   15 min  [low]     [ ]

After completing Morning walk (daily) and Medication (once)
--------------------------------------------------
09:00  Grooming      Mochi      20 min  [low]     [ ]
15:30  Playtime      Whiskers   15 min  [low]     [ ]
18:00  Evening walk  Mochi      30 min  [medium]  [ ]
18:00  Training      Mochi      15 min  [medium]  [ ]
07:30  Morning walk  Mochi      30 min  [high]    [ ]  due 2026-10-29
08:00  Feeding       Whiskers   10 min  [high]    [ ]  due 2026-10-29
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover:

- **Task basics:** `mark_complete()` changes a task's status, and adding a task to a pet increases its task count.
- **Sorting:** tasks from different pets come back in chronological order, and today's schedule skips tasks due on other days or when there are no tasks at all.
- **Recurrence:** completing a daily task creates a new task due the next day, and a weekly task one due 7 days later. One-time tasks create nothing, and completing a task twice does not create a duplicate.
- **Conflict detection:** tasks sharing a date and time are flagged, whether they belong to the same pet or different pets, and a warning lists every task involved. Different times, different days and completed tasks are not flagged.
- **Filtering:** by pet name (case-insensitive), by completion status, by both together, and an unknown pet returns an empty list.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\djain\Documents\BrownSchoolFiles\5. FAU\Courses by Semester\Fall 2026\Principles of Software Engineering\Codepath\Week 4\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 11 items

tests\test_pawpal.py ...........                                         [100%]

============================= 11 passed in 0.05s ==============================
```

**Confidence level: ★★★★☆ (4/5).** All 11 tests pass and the core behaviors (sorting, recurrence, conflict detection, filtering) are covered, including several edge cases. I did not give it 5 stars because conflict detection only matches exact times and does not catch overlapping durations.

## 📐 Smarter Scheduling

| Feature | Method(s) | How it works |
|---------|-----------|--------------|
| Sorting by time | `Scheduler.sort_by_time()`, `Scheduler.get_todays_schedule()` | Sorts on the "HH:MM" string with a lambda key. Ties keep their original order. Today's schedule keeps only tasks due today. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Filters by pet name (case-insensitive) and/or completion status. Both filters are optional and can be combined. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups incomplete tasks by date and time and returns a warning message for each group with more than one task. Covers same-pet and cross-pet clashes and never raises an error. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates a copy due 1 or 7 days after the original due date. Completing the same task twice does not create a duplicate. |

**Tradeoff:** conflicts are only flagged when two tasks share the exact same date and time. Overlapping durations are not checked. See section 2b of [reflection.md](reflection.md).

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
