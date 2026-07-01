from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TaskCategory(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"
    CLEANING = "cleaning"
    BEHAVIOR_RECORD = "behavior_record"
    HEALTH_CHECK = "health_check"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Frequency(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


class TaskStatus(Enum):
    PENDING = "pending"
    DONE = "done"
    OVERDUE = "overdue"
    MISSED = "missed"


_PRIORITY_ORDER = {
    Priority.CRITICAL: 0,
    Priority.HIGH: 1,
    Priority.MEDIUM: 2,
    Priority.LOW: 3,
}


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

@dataclass
class Task:
    id: int
    description: str
    category: TaskCategory
    scheduled_time: datetime
    priority: Priority
    frequency: Frequency = Frequency.ONCE
    duration_minutes: int = 15
    status: TaskStatus = TaskStatus.PENDING
    pet: "Pet | None" = None

    def mark_done(self) -> None:
        self.status = TaskStatus.DONE

    def mark_pending(self) -> None:
        self.status = TaskStatus.PENDING

    def is_overdue(self, now: datetime) -> bool:
        return self.status != TaskStatus.DONE and now > self.scheduled_time

    def refresh_status(self, now: datetime) -> TaskStatus:
        if self.status != TaskStatus.DONE and now > self.scheduled_time:
            self.status = TaskStatus.OVERDUE
        return self.status

    def reschedule(self, new_time: datetime) -> None:
        self.scheduled_time = new_time
        if self.status != TaskStatus.DONE:
            self.status = TaskStatus.PENDING

    def next_occurrence(self) -> "datetime | None":
        if self.frequency == Frequency.DAILY:
            return self.scheduled_time + timedelta(days=1)
        if self.frequency == Frequency.WEEKLY:
            return self.scheduled_time + timedelta(weeks=1)
        return None


@dataclass
class Pet:
    id: int
    name: str
    species: str
    breed: str = ""
    age: int = 0
    gender: str = ""
    health_notes: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks(self) -> list:
        return list(self.tasks)

    def get_tasks_by_status(self, status: TaskStatus) -> list:
        return [t for t in self.tasks if t.status == status]


@dataclass
class Owner:
    id: int
    name: str
    email: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pet(self, pet_id: int) -> "Pet | None":
        return next((p for p in self.pets if p.id == pet_id), None)

    def get_all_tasks(self) -> list:
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The "brain": retrieves, organizes, and manages tasks across pets."""

    def get_all_tasks(self, owner: Owner) -> list:
        return owner.get_all_tasks()

    def organize_by_pet(self, owner: Owner) -> dict:
        return {pet.id: pet.get_tasks() for pet in owner.pets}

    def sort_by_priority(self, tasks: list) -> list:
        return sorted(tasks, key=lambda t: (_PRIORITY_ORDER[t.priority], t.scheduled_time))

    def get_tasks_for_day(self, owner: Owner, day: date) -> list:
        tasks = [t for t in owner.get_all_tasks() if t.scheduled_time.date() == day]
        return self.sort_by_priority(tasks)

    def refresh_all_statuses(self, owner: Owner, now: datetime) -> None:
        for task in owner.get_all_tasks():
            task.refresh_status(now)

    def get_overdue_tasks(self, owner: Owner, now: datetime) -> list:
        self.refresh_all_statuses(owner, now)
        return [t for t in owner.get_all_tasks() if t.status == TaskStatus.OVERDUE]

    def mark_task_done(self, owner: Owner, task_id: int) -> "Task | None":
        for task in owner.get_all_tasks():
            if task.id == task_id:
                task.mark_done()
                return task
        return None


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class SchedulingTest:
    def test_high_priority_task_sorted_first(self):
        pass

    def test_overdue_task_detected(self):
        pass

    def test_tasks_grouped_by_pet(self):
        pass

    def test_mark_task_done_updates_status(self):
        pass

    def test_daily_plan_filters_by_date(self):
        pass
