from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    care_tasks: list[CareTask] = field(default_factory=list)
    schedules: list[DailySchedule] = field(default_factory=list)

    def add_care_task(self, task: CareTask) -> None:
        pass

    def remove_care_task(self, task: CareTask) -> None:
        pass


@dataclass(eq=False)
class CareTask:
    title: str
    duration_minutes: int
    priority: str


@dataclass
class DailySchedule:
    date: date
    available_minutes: int
    scheduled_times: dict[CareTask, datetime] = field(default_factory=dict)

    def build(self, pet: Pet) -> None:
        pass

    def explain(self) -> str:
        pass