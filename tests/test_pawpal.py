from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def make_task(time="08:00", frequency="once", due_date=None, description="Walk") -> Task:
    task = Task(
        description=description,
        time=time,
        duration_minutes=30,
        priority="high",
        frequency=frequency,
    )
    if due_date is not None:
        task.due_date = due_date
    return task


@pytest.fixture
def setup():
    """An owner with two pets and a scheduler."""
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    return owner, mochi, whiskers, Scheduler(owner)


def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(make_task())

    assert len(pet.get_tasks()) == 1


def test_schedule_is_sorted_chronologically_across_pets(setup):
    owner, mochi, whiskers, scheduler = setup
    mochi.add_task(make_task("18:00", description="Evening walk"))
    whiskers.add_task(make_task("09:00", description="Medication"))
    mochi.add_task(make_task("07:30", description="Morning walk"))

    times = [task.time for _, task in scheduler.get_todays_schedule()]

    assert times == ["07:30", "09:00", "18:00"]


def test_schedule_handles_no_tasks_and_skips_other_days(setup):
    owner, mochi, whiskers, scheduler = setup
    assert scheduler.get_todays_schedule() == []

    tomorrow = date.today() + timedelta(days=1)
    mochi.add_task(make_task("08:00", due_date=tomorrow))

    assert scheduler.get_todays_schedule() == []


@pytest.mark.parametrize("frequency, days", [("daily", 1), ("weekly", 7)])
def test_completing_recurring_task_creates_next_occurrence(setup, frequency, days):
    owner, mochi, whiskers, scheduler = setup
    task = make_task("08:00", frequency=frequency, description="Feeding")
    mochi.add_task(task)

    scheduler.mark_task_complete(mochi, task)

    assert task.completed is True
    assert len(mochi.get_tasks()) == 2
    new_task = mochi.get_tasks()[1]
    assert new_task.due_date == task.due_date + timedelta(days=days)
    assert new_task.completed is False
    assert (new_task.description, new_task.time) == ("Feeding", "08:00")


def test_one_time_task_creates_no_next_occurrence(setup):
    owner, mochi, whiskers, scheduler = setup
    task = make_task(frequency="once")
    mochi.add_task(task)

    scheduler.mark_task_complete(mochi, task)

    assert len(mochi.get_tasks()) == 1


def test_completing_twice_does_not_duplicate_recurring_task(setup):
    owner, mochi, whiskers, scheduler = setup
    task = make_task(frequency="daily")
    mochi.add_task(task)

    scheduler.mark_task_complete(mochi, task)
    scheduler.mark_task_complete(mochi, task)

    assert len(mochi.get_tasks()) == 2


def test_conflicts_flagged_for_same_pet_and_across_pets(setup):
    owner, mochi, whiskers, scheduler = setup
    mochi.add_task(make_task("09:00", description="Grooming"))
    mochi.add_task(make_task("09:00", description="Training"))  # same pet
    whiskers.add_task(make_task("09:00", description="Medication"))  # other pet
    whiskers.add_task(make_task("12:00", description="Playtime"))  # no clash

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    for name in ("Grooming", "Training", "Medication"):
        assert name in conflicts[0]
    assert "Playtime" not in conflicts[0]


def test_no_false_conflicts(setup):
    owner, mochi, whiskers, scheduler = setup
    tomorrow = date.today() + timedelta(days=1)
    mochi.add_task(make_task("09:00"))
    whiskers.add_task(make_task("09:00", due_date=tomorrow))  # same time, other day
    done = make_task("09:00")
    done.mark_complete()
    whiskers.add_task(done)  # same time, but already completed

    assert scheduler.detect_conflicts() == []


def test_filter_by_pet_and_status(setup):
    owner, mochi, whiskers, scheduler = setup
    done = make_task("07:00", description="Feeding")
    done.mark_complete()
    mochi.add_task(done)
    mochi.add_task(make_task("08:00", description="Walk"))
    whiskers.add_task(make_task("09:00", description="Medication"))

    assert len(scheduler.filter_tasks(pet_name="mochi")) == 2  # case-insensitive
    assert [t.description for _, t in scheduler.filter_tasks(completed=True)] == ["Feeding"]
    both = scheduler.filter_tasks(pet_name="Mochi", completed=False)
    assert [t.description for _, t in both] == ["Walk"]
    assert scheduler.filter_tasks(pet_name="Rex") == []
