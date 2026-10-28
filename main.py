from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, pairs: list[tuple[Pet, Task]]) -> None:
    print(f"\n{title}")
    print("-" * 50)
    if not pairs:
        print("(none)")
    for pet, task in pairs:
        status = "[x]" if task.completed else "[ ]"
        # Only show the date for tasks that aren't due today (e.g. recurring ones).
        due = "" if task.due_date == date.today() else f"  due {task.due_date}"
        print(
            f"{task.time}  {task.description:<14}{pet.name:<10}"
            f"{task.duration_minutes:>3} min  {'[' + task.priority + ']':<9} {status}{due}"
        )


def main() -> None:
    owner = Owner(name="D'Jaine")
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # Added out of order on purpose to show the schedule is sorted by time.
    evening_walk = Task("Evening walk", "18:00", 30, "medium", frequency="daily")
    morning_walk = Task("Morning walk", "07:30", 30, "high", frequency="daily")
    medication = Task("Medication", "09:00", 5, "high")
    feeding = Task("Feeding", "08:00", 10, "high", frequency="daily")
    playtime = Task("Playtime", "15:30", 15, "low")
    # These two collide with existing tasks: one across pets, one for the same pet.
    grooming = Task("Grooming", "09:00", 20, "low")
    training = Task("Training", "18:00", 15, "medium")

    mochi.add_task(evening_walk)
    mochi.add_task(morning_walk)
    mochi.add_task(grooming)
    mochi.add_task(training)
    whiskers.add_task(medication)
    whiskers.add_task(playtime)
    whiskers.add_task(feeding)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(whiskers, feeding)

    print_tasks(
        f"Today's Schedule for {owner.name} ({date.today()})",
        scheduler.get_todays_schedule(),
    )

    print("\nConflict warnings")
    print("-" * 50)
    conflicts = scheduler.detect_conflicts()
    for warning in conflicts:
        print(f"WARNING: {warning}")
    if not conflicts:
        print("(none)")

    print_tasks("Mochi's tasks", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")))
    print_tasks("Incomplete tasks", scheduler.sort_by_time(scheduler.filter_tasks(completed=False)))
    print_tasks("Completed tasks", scheduler.sort_by_time(scheduler.filter_tasks(completed=True)))
    print_tasks(
        "Whiskers' incomplete tasks",
        scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Whiskers", completed=False)),
    )

    # Completing a daily task adds the next day's occurrence; a one-time task adds nothing.
    scheduler.mark_task_complete(mochi, morning_walk)
    scheduler.mark_task_complete(mochi, morning_walk)  # repeat call must not duplicate it
    scheduler.mark_task_complete(whiskers, medication)
    print_tasks(
        "After completing Morning walk (daily) and Medication (once)",
        sorted(
            scheduler.filter_tasks(completed=False),
            key=lambda pair: (pair[1].due_date, pair[1].time),
        ),
    )


if __name__ == "__main__":
    main()
