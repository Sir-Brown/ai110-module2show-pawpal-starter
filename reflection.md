# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

*Add a pet*
The owner enters their own info and adds one or more pets (name, species), which are stored under that owner.

*Schedule a care task*
The owner chooses a pet and adds a task (walk, feeding, medication, appointment) with a time, duration, and priority, optionally repeating daily or weekly.

*View today's schedule*
The app combines tasks from all of the owner's pets into one list ordered by time, and warns about conflicts.


**a. Initial design**

I chose four classes. `Task` holds one care activity (description, time, duration, priority, frequency, due date, completion status). `Pet` stores a pet's name and species and owns a list of tasks. `Owner` holds a name and a list of pets and can gather every task across them. `Scheduler` takes an `Owner` and handles the logic: sorting, filtering, conflict detection, and completing recurring tasks. `Task`, `Pet` and `Owner` are dataclasses because they mostly hold data. `Scheduler` is a plain class because it holds behavior.

**b. Design changes**

After an AI review of the skeleton, I made `Task` compare by identity (`eq=False`) so two identical-looking tasks can't be confused when removing or completing one. I also decided that today's schedule and conflict checks must use `due_date` as well as `time`, since recurring tasks create future occurrences that shouldn't appear today or conflict with other days.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three things: when a task is due (date and time), whether it's completed, and how often it repeats (once, daily or weekly). It orders the day by time, flags tasks that share an exact date and time, and creates the next occurrence when a recurring task is finished. Tasks also store a duration and a priority; however, they don't affect ordering or conflict detection.

**b. Tradeoffs**

The scheduler only flags a conflict when two incomplete tasks have exactly the same date and time. It does not check whether durations overlap, so a 30-minute walk at 08:00 and a feeding at 08:15 would not be flagged, even though the walk is still going. I think this is reasonable because exact matches are simple to explain, easy to test, and never produce confusing false alarms. Overlap detection would need interval comparisons and extra decisions, such as whether back-to-back tasks count or whether two pets can be cared for at once. Essentially, it'd be harder to implement.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code inside VS Code as a collaborator for design, implementation and testing. I worked in a propose-then-approve loop: for each phase I asked for a proposal first (what would change, and which decisions were mine to make), approved or adjusted it, and only then let it edit files. The features that helped most were multi-file edits (the logic layer, `main.py` and `app.py` changing together) and being able to run the demo, the tests and a headless Streamlit check in the terminal. The most helpful prompts asked for a proposal with explicit tradeoffs, not just "write this".

**b. Judgment and verification**

A few moments where I didn't take a suggestion as-is:

- For recurrence, the course hint says the next due date is "today + 1 day". I used `due_date + 1 day` instead, so a daily task completed late keeps its rhythm instead of skipping a day.
- The AI offered a more compact `groupby` version of `detect_conflicts`. It needed sorting first, repeated the key and was harder to read, so I kept the simpler dictionary version.
- I turned down overlapping-duration conflict detection because it was more complex than this project needed.
- The AI's Phase 3 UI passed its own headless check, but when I used the app myself I noticed there was no way to mark a task complete. The AI had missed that. I caught it, and it became part of the Phase 6 UI work.

---

## 4. Testing and Verification

**a. What you tested**

I tested sorting across pets, today's schedule, daily and weekly recurrence, conflicts, and filtering by pet and status. These matter because they're the behaviors the owner relies on, and several of them are where scheduling bugs usually hide.

**b. Confidence**

I'm at 4 out of 5. All 11 tests pass and the core behaviors are covered, but conflict detection only catches exact time matches. Next I'd test overlapping durations, time-format validation (a time like "9:00" would sort after "10:00"), invalid priority or frequency values, and removing a task that a pet doesn't have.

---

## 5. Reflection

**a. What went well**

I'm most satisfied that the logic in `pawpal_system.py` stayed independent of the interface. The same classes worked unchanged in the CLI demo, the tests and the Streamlit app, which made each new layer easy to build and check.

**b. What you would improve**

If I had another iteration, I'd use priority and duration for real: sorting by priority, detecting overlapping tasks, and suggesting the next free slot. I'd also validate the time format, make the owner's data persist between runs, and add the explanation of the plan that the scenario describes, which I didn't build.

**c. Key takeaway**

Working with a powerful AI doesn't remove the need to be the architect. It writes code quickly, but I had to decide the scope, the tradeoffs and what "good enough" meant, and I had to verify things myself, because the AI's own checks missed a gap I found by simply using the app.