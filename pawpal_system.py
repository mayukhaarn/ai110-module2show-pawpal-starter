from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    weight: Optional[float] = None
    needs: List[str] = field(default_factory=list)
    owner: Optional['Owner'] = None

    def add_need(self, need: str) -> None:
        if need not in self.needs:
            self.needs.append(need)

    def remove_need(self, need: str) -> None:
        if need in self.needs:
            self.needs.remove(need)

    def get_care_requirements(self) -> List[str]:
        return self.needs.copy()

    def describe(self) -> str:
        desc = f"{self.name} is a {self.species}"
        if self.age:
            desc += f" aged {self.age}"
        if self.weight:
            desc += f" weighing {self.weight} kg"
        return desc


@dataclass
class Task:
    title: str
    description: Optional[str] = None
    duration_minutes: int
    priority: str
    category: str
    pet: Pet
    due_time: Optional[datetime] = None
    is_recurring: bool = False
    status: str = "pending"

    def compute_score(self) -> float:
        priority_scores = {"low": 1, "medium": 2, "high": 3}
        score = priority_scores.get(self.priority, 1)
        if self.is_overdue(datetime.now()):
            score += 1
        return score

    def mark_complete(self) -> None:
        self.status = "completed"

    def is_overdue(self, now: datetime) -> bool:
        if self.due_time:
            return now > self.due_time
        return False

    def estimate_end(self, start: datetime) -> datetime:
        return start + timedelta(minutes=self.duration_minutes)


@dataclass
class ScheduledItem:
    task: Task
    start_time: datetime
    end_time: datetime
    assigned_owner: 'Owner'
    notes: Optional[str] = None

    def duration(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() / 60)

    def overlaps(self, other: 'ScheduledItem') -> bool:
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)

    def to_dict(self) -> Dict:
        return {
            "task_title": self.task.title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "assigned_owner": self.assigned_owner.name,
            "notes": self.notes
        }


class Owner:
    def __init__(self, name: str, email: Optional[str] = None, preferences: Optional[Dict] = None):
        self.name = name
        self.email = email
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: Pet) -> None:
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def get_daily_availability(self, date: date) -> int:
        return self.preferences.get('daily_hours', 8) * 60  # minutes

    def owns(self, pet: Pet) -> bool:
        return pet in self.pets


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.pets = owner.pets.copy()
        self.tasks: List[Task] = []
        self.schedule: List[ScheduledItem] = []
        self.constraints: Dict = {}

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)

    def build_daily_schedule(self, date: date) -> List[ScheduledItem]:
        available_minutes = self.owner.get_daily_availability(date)
        sorted_tasks = sorted(self.tasks, key=lambda t: t.compute_score(), reverse=True)
        current_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=8)  # start at 8am
        schedule = []
        for task in sorted_tasks:
            if task.status != "pending":
                continue
            if task.duration_minutes > available_minutes:
                continue
            end_time = current_time + timedelta(minutes=task.duration_minutes)
            item = ScheduledItem(task, current_time, end_time, self.owner)
            schedule.append(item)
            current_time = end_time
            available_minutes -= task.duration_minutes
        self.schedule = schedule
        return schedule

    def score_task(self, task: Task) -> float:
        return task.compute_score()

    def explain_plan(self) -> str:
        explanation = "Daily schedule explanation:\n"
        for item in self.schedule:
            explanation += f"- {item.task.title} at {item.start_time.strftime('%H:%M')} (priority: {item.task.priority})\n"
        return explanation

    def get_conflicts(self) -> List[ScheduledItem]:
        conflicts = []
        for i, item1 in enumerate(self.schedule):
            for item2 in self.schedule[i+1:]:
                if item1.overlaps(item2):
                    conflicts.extend([item1, item2])
        return conflicts

    def clear_schedule(self) -> None:
        self.schedule = []