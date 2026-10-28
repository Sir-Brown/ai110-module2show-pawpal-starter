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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
