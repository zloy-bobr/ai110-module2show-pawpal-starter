from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time as TimeOfDay


_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass(eq=False)
class Task:
    description: str
    time: TimeOfDay | None = None
    frequency: str = "daily"
    completed: bool = False
    duration_minutes: int = 1
    priority: str = "medium"

    def __post_init__(self) -> None:
        """Validate task fields."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if self.duration_minutes < 1:
            raise ValueError("Task duration must be at least one minute.")
        if not self.frequency.strip():
            raise ValueError("Task frequency cannot be empty.")
        if self.priority not in _PRIORITY_ORDER:
            raise ValueError("Priority must be 'low', 'medium', or 'high'.")


@dataclass(eq=False)
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task unless it is already assigned to this pet."""
        if task in self.tasks:
            raise ValueError("Task is already assigned to this pet.")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task assigned to this pet."""
        try:
            self.tasks.remove(task)
        except ValueError as error:
            raise ValueError("Task is not assigned to this pet.") from error


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        if pet in self.pets:
            raise ValueError("Pet is already registered to this owner.")
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Unregister a pet from this owner."""
        try:
            self.pets.remove(pet)
        except ValueError as error:
            raise ValueError("Pet is not registered to this owner.") from error

    def get_all_tasks(self) -> list[Task]:
        """Return tasks belonging to all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    owner: Owner

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks managed by this scheduler's owner."""
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks across the owner's pets."""
        return [task for task in self.owner.get_all_tasks() if not task.completed]

    def organize_tasks(self, include_completed: bool = False) -> list[Task]:
        """Return owner tasks ordered by time and then priority."""
        tasks = self.owner.get_all_tasks()
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]

        return sorted(
            tasks,
            key=lambda task: (
                task.time is None,
                task.time or TimeOfDay.max,
                _PRIORITY_ORDER[task.priority],
                task.description.casefold(),
            ),
        )

    def mark_complete(self, task: Task) -> None:
        """Mark one of the owner's tasks as complete."""
        if not any(owned_task is task for owned_task in self.owner.get_all_tasks()):
            raise ValueError("Task does not belong to one of this owner's pets.")
        task.completed = True