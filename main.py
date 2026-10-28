from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(scheduler: Scheduler) -> None:
    print(f"Today's Schedule for {scheduler.owner.name} ({date.today()})")
    print("-" * 50)
    for pet, task in scheduler.get_todays_schedule():
        status = "[x]" if task.completed else "[ ]"
        print(
            f"{task.time}  {task.description:<14}{pet.name:<10}"
            f"{task.duration_minutes:>3} min  {'[' + task.priority + ']':<9} {status}"
        )


def main() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # Added out of order on purpose to show the schedule is sorted by time.
    evening_walk = Task("Evening walk", "18:00", 30, "medium", frequency="daily")
    morning_walk = Task("Morning walk", "07:30", 30, "high", frequency="daily")
    medication = Task("Medication", "09:00", 5, "high")
    feeding = Task("Feeding", "08:00", 10, "high", frequency="daily")

    mochi.add_task(evening_walk)
    mochi.add_task(morning_walk)
    whiskers.add_task(medication)
    whiskers.add_task(feeding)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(whiskers, feeding)

    print_schedule(scheduler)


if __name__ == "__main__":
    main()
