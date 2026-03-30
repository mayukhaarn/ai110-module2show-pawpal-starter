# 🐾 PawPal+ Smart Pet Care Management System

PawPal+ is a smart pet care management system that helps owners keep their furry friends happy and healthy. The app tracks daily routines — feedings, walks, medications, and appointments — while using algorithmic logic to organize and prioritize tasks.

## 🚀 Features

- **Add Pets & Tasks** — Register multiple pets and schedule tasks with time, frequency, and priority
- **Sorting by Time** — All tasks are automatically sorted chronologically using Python's `sorted()` with a lambda key on "HH:MM" strings
- **Filter by Pet / Status / Priority** — Quickly find tasks for a specific pet, view only pending work, or focus on high-priority items
- **Recurring Task Automation** — Daily and weekly tasks automatically reschedule themselves when marked complete using Python's `timedelta`
- **Conflict Warnings** — The Scheduler detects two tasks at the same time and surfaces a warning rather than crashing
- **Streamlit UI** — A modern, interactive web interface with persistent state via `st.session_state`
- **CLI Demo Script** — A `main.py` script lets you verify backend logic directly in the terminal

## 🗂️ Project Structure

```
ai110-module2show-pawpal-starter/
├── pawpal_system.py   # Core logic: Task, Pet, Owner, Scheduler classes
├── app.py             # Streamlit UI
├── main.py            # CLI demo/testing script
├── tests/
│   └── test_pawpal.py # Automated pytest suite (17 tests)
├── requirements.txt
└── README.md
```

## ⚙️ Setup & Run

```bash
# Clone your fork and open in VS Code / Codespaces
git clone <your-fork-url>
cd ai110-module2show-pawpal-starter

# Install dependencies
pip install -r requirements.txt

# Run the CLI demo
python main.py

# Launch the Streamlit app
streamlit run app.py
```

## 🧠 Smarter Scheduling

PawPal+'s `Scheduler` class adds intelligence beyond simple task storage:

**Sorting by Time** — `sort_by_time()` uses Python's `sorted()` with a lambda key, sorting "HH:MM" strings lexicographically (which maps directly to chronological order):
```python
sorted(tasks, key=lambda t: t.time)
```

**Filtering** — `filter_by_pet()`, `filter_by_status()`, and `filter_by_priority()` use list comprehensions for readable, efficient filtering.

**Recurring Tasks** — When `mark_complete()` is called on a `daily` or `weekly` task, it automatically creates a new `Task` instance for the next occurrence using `timedelta`:
```python
next_due = self.due_date + timedelta(days=1)  # for daily tasks
```

**Conflict Detection** — `detect_conflicts()` scans pending tasks and returns human-readable warning strings (rather than raising exceptions) when two tasks share the same time slot. This is a lightweight O(n) strategy using a dictionary lookup.

*Tradeoff noted:* The current conflict detection only flags exact time matches, not overlapping durations. A more advanced implementation would compare `start_time + duration` against other tasks' windows — future work!

## 🧪 Testing PawPal+

The automated test suite covers all critical behaviors:

```bash
python -m pytest
```

Tests cover: task completion status change, task addition to a pet, chronological sort correctness, out-of-order task sorting, filtering by pet/status/priority, daily recurrence scheduling, weekly recurrence scheduling, one-time task returning None on completion, conflict detection with duplicate times, conflict detection with no conflicts, recurring tasks added via Scheduler, owner pet lookup, `get_all_tasks` across multiple pets, and `get_pending_tasks` on a pet.

**Confidence Level: ⭐⭐⭐⭐⭐ (5/5)** — All 17 tests pass. Core behaviors, edge cases (empty pet, no conflicts, one-time tasks), and algorithmic features are fully verified.

## 📸 Demo

Add pets and tasks via the sidebar, then view your sorted schedule with conflict warnings and one-click completion in the main panel.

## 🔧 Suggested Workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
