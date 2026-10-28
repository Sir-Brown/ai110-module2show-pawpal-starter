from pawpal_system import Pet, Task


def make_task() -> Task:
    return Task(description="Walk", time="08:00", duration_minutes=30, priority="high")


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
