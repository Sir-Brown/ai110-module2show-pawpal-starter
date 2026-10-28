from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(eq=False)
class Task:
    """A single pet care activity with a time, duration, priority and recurrence."""

    description: str
    time: str  # "HH:MM"
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    frequency: str = "once"  # "once" | "daily" | "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Task | None:
        """Return a new task for the next daily or weekly occurrence, or None for one-time tasks."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet and the care tasks assigned to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)


@dataclass
class Owner:
    """A pet owner and the pets they care for."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet | None:
        """Return the pet with the given name (case-insensitive), or None if not found."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task across all pets as (pet, task) pairs."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_todays_schedule(self) -> list[tuple[Pet, Task]]:
        """Return today's tasks for all pets, sorted by time."""
        today = date.today()
        todays = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if task.due_date == today
        ]
        return self.sort_by_time(todays)

    def sort_by_time(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs sorted by their "HH:MM" time."""
        return sorted(tasks, key=lambda pair: pair[1].time)

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs filtered by pet name and/or completion status."""
        raise NotImplementedError

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same time."""
        raise NotImplementedError

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Mark a pet's task as completed."""
        task.mark_complete()
