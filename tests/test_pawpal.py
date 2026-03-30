"""
tests/test_pawpal.py - Automated test suite for PawPal+ system.
Run with: python -m pytest
"""
import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_owner():
    """Return an owner with two pets and several tasks."""
    owner = Owner(name="Test Owner", email="test@example.com")
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese", age=5)
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    return owner


@pytest.fixture
def sample_tasks(sample_owner):
    """Add sample tasks to the owner's pets and return scheduler."""
    buddy = sample_owner.pets[0]
    whiskers = sample_owner.pets[1]
    today = date.today()

    buddy.add_task(Task(
        title="Morning Feed",
        time="08:00",
        pet_name="Buddy",
        frequency="daily",
        priority="high",
        due_date=today,
    ))
    buddy.add_task(Task(
        title="Afternoon Walk",
        time="15:00",
        pet_name="Buddy",
        frequency="once",
        priority="medium",
        due_date=today,
    ))
    whiskers.add_task(Task(
        title="Breakfast",
        time="08:00",
        pet_name="Whiskers",
        frequency="daily",
        priority="high",
        due_date=today,
    ))
    whiskers.add_task(Task(
        title="Vet Appointment",
        time="14:00",
        pet_name="Whiskers",
        frequency="once",
        priority="high",
        due_date=today,
    ))
    return Scheduler(sample_owner)


# ─── Phase 2: Task Completion and Addition ────────────────────────────────────

def test_task_completion_changes_status():
    """Verify mark_complete() changes is_complete to True."""
    task = Task(title="Feed", time="08:00", pet_name="Buddy")
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_task_addition_increases_pet_task_count():
    """Verify that adding a task to a Pet increases task count."""
    pet = Pet(name="Buddy", species="Dog")
    initial_count = len(pet.tasks)
    pet.add_task(Task(title="Walk", time="09:00", pet_name="Buddy"))
    assert len(pet.tasks) == initial_count + 1


# ─── Phase 4 & 5: Sorting, Filtering, Recurring, Conflict Detection ──────────

def test_sort_by_time_returns_chronological_order(sample_tasks):
    """Verify tasks are sorted in ascending HH:MM order."""
    sorted_tasks = sample_tasks.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times), f"Expected sorted times, got: {times}"


def test_sort_by_time_with_out_of_order_tasks():
    """Verify sorting works when tasks are added out of order."""
    owner = Owner("Test")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Evening Walk", time="18:00", pet_name="Rex"))
    pet.add_task(Task(title="Morning Feed", time="07:00", pet_name="Rex"))
    pet.add_task(Task(title="Noon Meds", time="12:00", pet_name="Rex"))
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    assert [t.time for t in sorted_tasks] == ["07:00", "12:00", "18:00"]


def test_filter_by_pet_returns_only_that_pets_tasks(sample_tasks):
    """Verify filtering by pet name only returns tasks for that pet."""
    buddy_tasks = sample_tasks.filter_by_pet("Buddy")
    assert all(t.pet_name == "Buddy" for t in buddy_tasks)
    assert len(buddy_tasks) == 2


def test_filter_by_status_returns_pending_tasks(sample_tasks):
    """Verify filtering by completed=False returns only pending tasks."""
    pending = sample_tasks.filter_by_status(completed=False)
    assert all(not t.is_complete for t in pending)


def test_filter_by_status_returns_completed_tasks(sample_tasks):
    """Verify filtering by completed=True returns completed tasks."""
    # Complete one task first
    task = sample_tasks.owner.pets[0].tasks[0]
    task.is_complete = True
    completed = sample_tasks.filter_by_status(completed=True)
    assert len(completed) == 1
    assert completed[0].is_complete is True


def test_filter_by_pet_empty_for_unknown_pet(sample_tasks):
    """Verify filtering for unknown pet returns empty list."""
    result = sample_tasks.filter_by_pet("NoSuchPet")
    assert result == []


def test_recurrence_daily_creates_next_task():
    """Confirm marking a daily task complete creates a new task for next day."""
    today = date.today()
    task = Task(
        title="Morning Feed",
        time="08:00",
        pet_name="Buddy",
        frequency="daily",
        due_date=today,
    )
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_complete is False
    assert next_task.title == "Morning Feed"


def test_recurrence_weekly_creates_next_task():
    """Confirm marking a weekly task complete creates a new task one week later."""
    today = date.today()
    task = Task(
        title="Bath Time",
        time="10:00",
        pet_name="Buddy",
        frequency="weekly",
        due_date=today,
    )
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_recurrence_once_returns_none():
    """Confirm that a one-time task returns None when marked complete."""
    task = Task(title="Vet Visit", time="14:00", pet_name="Buddy", frequency="once")
    result = task.mark_complete()
    assert result is None


def test_conflict_detection_flags_duplicate_times(sample_tasks):
    """Verify that the Scheduler flags tasks at the exact same time."""
    conflicts = sample_tasks.detect_conflicts()
    # Buddy Morning Feed and Whiskers Breakfast are both at 08:00
    assert len(conflicts) > 0
    assert "08:00" in conflicts[0]


def test_conflict_detection_no_conflicts():
    """Verify no conflicts when all tasks are at different times."""
    owner = Owner("Solo")
    pet = Pet(name="Fido", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Feed", time="08:00", pet_name="Fido"))
    pet.add_task(Task(title="Walk", time="09:00", pet_name="Fido"))
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert conflicts == []


def test_scheduler_mark_task_complete_adds_recurring(sample_tasks):
    """Verify mark_task_complete adds recurring next task to the pet."""
    buddy = sample_tasks.owner.pets[0]
    morning_feed = buddy.tasks[0]  # "Morning Feed", daily
    count_before = len(buddy.tasks)
    sample_tasks.mark_task_complete(morning_feed)
    assert len(buddy.tasks) == count_before + 1
    assert buddy.tasks[-1].is_complete is False


def test_owner_add_and_get_pet():
    """Verify adding a pet to owner and retrieving it by name."""
    owner = Owner("Sam")
    pet = Pet(name="Luna", species="Dog")
    owner.add_pet(pet)
    found = owner.get_pet_by_name("Luna")
    assert found is not None
    assert found.name == "Luna"


def test_owner_get_all_tasks(sample_tasks):
    """Verify get_all_tasks returns tasks from all pets."""
    all_tasks = sample_tasks.owner.get_all_tasks()
    assert len(all_tasks) == 4


def test_pet_get_pending_tasks():
    """Verify get_pending_tasks only returns incomplete tasks."""
    pet = Pet(name="Max", species="Dog")
    t1 = Task(title="Feed", time="08:00", pet_name="Max")
    t2 = Task(title="Walk", time="09:00", pet_name="Max")
    t1.is_complete = True
    pet.add_task(t1)
    pet.add_task(t2)
    pending = pet.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].title == "Walk"
