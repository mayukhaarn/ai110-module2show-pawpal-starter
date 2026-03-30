"""
main.py - CLI demo script for PawPal+ system.
Run with: python main.py
"""
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    """Demonstrate PawPal+ system with owners, pets, and tasks."""
    # Create an owner
    owner = Owner(name="Alex Johnson", email="alex@example.com")

    # Create two pets
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese", age=5)

    # Add pets to owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Add tasks in non-chronological order (to demonstrate sorting)
    buddy.add_task(Task(
        title="Afternoon Walk",
        time="15:00",
        pet_name="Buddy",
        description="30-minute walk in the park",
        frequency="daily",
        duration_minutes=30,
        priority="high",
        category="exercise",
        due_date=date.today(),
    ))
    buddy.add_task(Task(
        title="Morning Feed",
        time="08:00",
        pet_name="Buddy",
        description="Cup of dry kibble",
        frequency="daily",
        duration_minutes=10,
        priority="high",
        category="feeding",
        due_date=date.today(),
    ))
    buddy.add_task(Task(
        title="Flea Treatment",
        time="10:00",
        pet_name="Buddy",
        description="Monthly flea prevention",
        frequency="once",
        duration_minutes=15,
        priority="medium",
        category="medication",
        due_date=date.today(),
    ))

    whiskers.add_task(Task(
        title="Breakfast",
        time="08:00",
        pet_name="Whiskers",
        description="Wet food serving",
        frequency="daily",
        duration_minutes=5,
        priority="high",
        category="feeding",
        due_date=date.today(),
    ))
    whiskers.add_task(Task(
        title="Vet Appointment",
        time="14:00",
        pet_name="Whiskers",
        description="Annual checkup",
        frequency="once",
        duration_minutes=60,
        priority="high",
        category="medical",
        due_date=date.today(),
    ))

    # Create a scheduler
    scheduler = Scheduler(owner)

    # Print today's schedule (sorted by time)
    print("\n" + "=" * 55)
    print("        PawPal+ Today's Schedule Demo")
    print("=" * 55)
    schedule = scheduler.sort_by_time(scheduler.get_all_tasks())
    for task in schedule:
        print(f"  {task}")
    print("=" * 55)

    # Demonstrate filtering by pet
    print("\n[Filter] Tasks for Buddy:")
    for task in scheduler.filter_by_pet("Buddy"):
        print(f"  {task}")

    # Demonstrate filtering by status
    print("\n[Filter] Pending tasks:")
    for task in scheduler.filter_by_status(completed=False):
        print(f"  {task}")

    # Demonstrate conflict detection
    print("\n[Conflicts]")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")

    # Demonstrate recurring task (mark Buddy morning feed complete)
    print("\n[Recurring] Marking Buddy's Morning Feed complete...")
    morning_feed = buddy.tasks[1]  # Morning Feed
    next_task = scheduler.mark_task_complete(morning_feed)
    if next_task:
        print(f"  Next occurrence scheduled: {next_task.title} on {next_task.due_date} at {next_task.time}")

    print("\n[Demo complete]")


if __name__ == "__main__":
    main()
