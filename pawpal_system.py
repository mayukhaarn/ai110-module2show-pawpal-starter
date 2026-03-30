"""
PawPal+ System: Core logic layer for pet care management.
Implements Owner, Pet, Task, and Scheduler classes with
sorting, filtering, recurring tasks, and conflict detection.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    time: str  # "HH:MM" format
    pet_name: str
    description: str = ""
    frequency: str = "once"  # "once", "daily", "weekly"
    duration_minutes: int = 30
    priority: str = "medium"  # "low", "medium", "high"
    category: str = "general"
    is_complete: bool = False
    due_date: Optional[date] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark task complete and return next occurrence for recurring tasks."""
        self.is_complete = True
        if self.frequency == "daily":
            next_due = (self.due_date or date.today()) + timedelta(days=1)
            return Task(
                title=self.title,
                time=self.time,
                pet_name=self.pet_name,
                description=self.description,
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                category=self.category,
                is_complete=False,
                due_date=next_due,
            )
        elif self.frequency == "weekly":
            next_due = (self.due_date or date.today()) + timedelta(weeks=1)
            return Task(
                title=self.title,
                time=self.time,
                pet_name=self.pet_name,
                description=self.description,
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                category=self.category,
                is_complete=False,
                due_date=next_due,
            )
        return None

    def __str__(self) -> str:
        """Return readable string representation of the task."""
        status = "✓" if self.is_complete else "○"
        return f"[{status}] {self.time} - {self.title} ({self.pet_name}) [{self.priority}]"


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return only incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.is_complete]

    def __str__(self) -> str:
        """Return readable string of pet info."""
        return f"{self.name} ({self.species}, {self.breed}, age {self.age})"


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str, email: str = "", preferences: Optional[Dict] = None):
        """Initialize owner with name, email, and optional preferences."""
        self.name = name
        self.email = email
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's list."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        """Find and return a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def __str__(self) -> str:
        """Return readable string of owner info."""
        return f"Owner: {self.name} ({len(self.pets)} pets)"


class Scheduler:
    """The brain that retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks chronologically by their HH:MM time string."""
        task_list = tasks if tasks is not None else self.get_all_tasks()
        return sorted(task_list, key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filter tasks by pet name (case-insensitive)."""
        return [t for t in self.get_all_tasks() if t.pet_name.lower() == pet_name.lower()]

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        return [t for t in self.get_all_tasks() if t.is_complete == completed]

    def filter_by_priority(self, priority: str) -> List[Task]:
        """Filter tasks by priority level (low, medium, high)."""
        return [t for t in self.get_all_tasks() if t.priority.lower() == priority.lower()]

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Detect tasks scheduled at the same time and return warning messages."""
        task_list = tasks if tasks is not None else self.get_all_tasks()
        pending = [t for t in task_list if not t.is_complete]
        warnings = []
        seen: Dict[str, Task] = {}
        for task in pending:
            key = task.time
            if key in seen:
                other = seen[key]
                warnings.append(
                    f"⚠ Conflict at {task.time}: '{task.title}' ({task.pet_name}) "
                    f"clashes with '{other.title}' ({other.pet_name})"
                )
            else:
                seen[key] = task
        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete, auto-schedule next if recurring."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet = self.owner.get_pet_by_name(task.pet_name)
            if pet:
                pet.add_task(next_task)
        return next_task

    def get_todays_schedule(self) -> List[Task]:
        """Return all pending tasks sorted by time for today's schedule."""
        today = date.today()
        tasks = self.get_all_tasks()
        todays = [
            t for t in tasks
            if not t.is_complete and (t.due_date is None or t.due_date == today)
        ]
        return self.sort_by_time(todays)

    def print_schedule(self, tasks: Optional[List[Task]] = None) -> None:
        """Print a formatted schedule to the terminal."""
        schedule = tasks if tasks is not None else self.get_todays_schedule()
        print("=" * 50)
        print("         PawPal+ Today's Schedule")
        print("=" * 50)
        if not schedule:
            print("  No tasks scheduled for today.")
        else:
            for task in schedule:
                print(f"  {task}")
        print("=" * 50)
