from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time as TimeOfDay, timedelta


_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass(eq=False)
class Task:
    description: str
    time: TimeOfDay | None = None
    frequency: str = "daily"
    recurrence_start: date = field(default_factory=date.today)
    completed: bool = False
    duration_minutes: int = 1
    priority: str = "medium"

    def __post_init__(self) -> None:
        """Validate task fields."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if self.duration_minutes < 1:
            raise ValueError("Task duration must be at least one minute.")
        if self.frequency not in {"daily", "weekly", "as needed"}:
            raise ValueError("Frequency must be 'daily', 'weekly', or 'as needed'.")
        if self.priority not in _PRIORITY_ORDER:
            raise ValueError("Priority must be 'low', 'medium', or 'high'.")

    def occurs_on(self, day: date) -> bool:
        """Return whether this task recurs on the given date."""
        if day < self.recurrence_start:
            return False
        if self.frequency in {"daily", "as needed"}:
            return True
        return (day - self.recurrence_start).days % 7 == 0


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

    def filter_tasks(
        self,
        pet: Pet | None = None,
        pet_name: str | None = None,
        completed: bool | None = None,
        on_date: date | None = None,
    ) -> list[Task]:
        """Filter owner tasks by pet, pet name, status, and recurrence date."""
        tasks = self.owner.get_all_tasks()
        if pet is not None:
            if not any(owned_pet is pet for owned_pet in self.owner.pets):
                raise ValueError("Pet does not belong to this owner.")
            tasks = [task for task in tasks if task in pet.tasks]
        if pet_name is not None:
            normalized_name = pet_name.strip().casefold()
            if not normalized_name:
                raise ValueError("Pet name filter cannot be empty.")
            matching_pets = [
                owned_pet
                for owned_pet in self.owner.pets
                if owned_pet.name.casefold() == normalized_name
            ]
            tasks = [
                task
                for task in tasks
                if any(task in matching_pet.tasks for matching_pet in matching_pets)
            ]
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        if on_date is not None:
            tasks = [task for task in tasks if task.occurs_on(on_date)]
        return tasks

    def get_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks across the owner's pets."""
        return self.filter_tasks(completed=False)

    def organize_tasks(
        self,
        include_completed: bool = False,
        pet: Pet | None = None,
        on_date: date | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return owner tasks ordered by time and then priority."""
        completed_filter = (
            completed
            if completed is not None
            else None if include_completed else False
        )
        tasks = self.filter_tasks(
            pet=pet,
            completed=completed_filter,
            on_date=on_date,
        )

        return sorted(
            tasks,
            key=lambda task: (
                task.time is None,
                task.time or TimeOfDay.max,
                _PRIORITY_ORDER[task.priority],
                task.description.casefold(),
            ),
        )

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Sort tasks by zero-padded HH:MM time, placing unscheduled tasks last."""
        tasks_to_sort = self.owner.get_all_tasks() if tasks is None else tasks
        return sorted(
            tasks_to_sort,
            key=lambda task: (
                task.time is None,
                task.time.strftime("%H:%M") if task.time is not None else "",
            ),
        )

    def find_conflicts(
        self,
        on_date: date,
        pet: Pet | None = None,
    ) -> list[tuple[Task, Task]]:
        """Return overlapping timed task pairs for a date."""
        tasks = self.filter_tasks(pet=pet, completed=False, on_date=on_date)
        intervals = sorted(
            (
                (
                    task.time.hour * 60 + task.time.minute,
                    task.time.hour * 60 + task.time.minute + task.duration_minutes,
                    task,
                )
                for task in tasks
                if task.time is not None
            ),
            key=lambda interval: (interval[0], interval[1]),
        )
        active: list[tuple[int, int, Task]] = []
        conflicts: list[tuple[Task, Task]] = []

        for start, end, task in intervals:
            active = [interval for interval in active if interval[1] > start]
            conflicts.extend((overlapping_task, task) for _, _, overlapping_task in active)
            active.append((start, end, task))

        return conflicts

    def get_conflict_warnings(
        self,
        on_date: date,
        pet: Pet | None = None,
    ) -> list[str]:
        """Return readable warnings for overlapping tasks without raising."""
        task_pets = {
            task: owned_pet
            for owned_pet in self.owner.pets
            for task in owned_pet.tasks
        }
        return [
            (
                f"{task_pets[first_task].name}'s {first_task.description} at "
                f"{first_task.time:%H:%M} overlaps with "
                f"{task_pets[second_task].name}'s {second_task.description} at "
                f"{second_task.time:%H:%M}."
            )
            for first_task, second_task in self.find_conflicts(on_date, pet)
        ]

    def mark_complete(self, task: Task, today: date | None = None) -> Task | None:
        """Complete an owned task and create its next daily or weekly occurrence."""
        owning_pet = next(
            (
                pet
                for pet in self.owner.pets
                if any(owned_task is task for owned_task in pet.tasks)
            ),
            None,
        )
        if owning_pet is None:
            raise ValueError("Task does not belong to one of this owner's pets.")
        if task.completed:
            return None

        task.completed = True
        if task.frequency not in {"daily", "weekly"}:
            return None

        completion_date = today if today is not None else date.today()
        recurrence_days = 1 if task.frequency == "daily" else 7
        next_task = Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            recurrence_start=completion_date + timedelta(days=recurrence_days),
            duration_minutes=task.duration_minutes,
            priority=task.priority,
        )
        owning_pet.add_task(next_task)
        return next_task