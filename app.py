"""
app.py - Streamlit UI for PawPal+ pet care management system.
Run with: streamlit run app.py
"""
import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# ─── Session State: Initialize Owner ─────────────────────────────────────────
# st.session_state acts as a persistent dictionary across reruns.
# We check before creating so data is not wiped on every interaction.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="My Household")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

# ─── Sidebar: Add a Pet ───────────────────────────────────────────────────────
st.sidebar.header("🐾 Add a Pet")
with st.sidebar.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet Name", placeholder="e.g. Buddy")
    species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
    breed = st.text_input("Breed", placeholder="e.g. Labrador")
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
    submitted_pet = st.form_submit_button("Add Pet")
    if submitted_pet and pet_name:
        if owner.get_pet_by_name(pet_name) is None:
            new_pet = Pet(name=pet_name, species=species, breed=breed, age=age)
            owner.add_pet(new_pet)
            st.success(f"Added {pet_name} the {species}!")
        else:
            st.warning(f"{pet_name} already exists.")

# ─── Sidebar: Add a Task ──────────────────────────────────────────────────────
st.sidebar.header("📋 Schedule a Task")
pet_names = [p.name for p in owner.pets]
if pet_names:
    with st.sidebar.form("add_task_form", clear_on_submit=True):
        task_pet = st.selectbox("Pet", pet_names)
        task_title = st.text_input("Task Title", placeholder="e.g. Morning Walk")
        task_time = st.text_input("Time (HH:MM)", placeholder="08:00")
        task_freq = st.selectbox("Frequency", ["once", "daily", "weekly"])
        task_priority = st.selectbox("Priority", ["low", "medium", "high"])
        task_category = st.selectbox("Category", ["feeding", "exercise", "medication", "medical", "grooming", "general"])
        task_due = st.date_input("Due Date", value=date.today())
        submitted_task = st.form_submit_button("Add Task")
        if submitted_task and task_title and task_time:
            pet = owner.get_pet_by_name(task_pet)
            if pet:
                new_task = Task(
                    title=task_title,
                    time=task_time,
                    pet_name=task_pet,
                    frequency=task_freq,
                    priority=task_priority,
                    category=task_category,
                    due_date=task_due,
                )
                pet.add_task(new_task)
                st.success(f"Scheduled '{task_title}' for {task_pet}!")
else:
    st.sidebar.info("Add a pet first to schedule tasks.")

# ─── Main Area ────────────────────────────────────────────────────────────────
st.title("🐾 PawPal+ Smart Pet Care Manager")
st.caption(f"Managing {len(owner.pets)} pet(s) • {len(owner.get_all_tasks())} total task(s)")

# ── Conflict Warnings ─────────────────────────────────────────────────────────
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.subheader("⚠️ Schedule Conflicts Detected")
    for warning in conflicts:
        st.warning(warning)

# ── Today's Sorted Schedule ──────────────────────────────────────────────────
st.subheader("📅 Today's Schedule")

col1, col2, col3 = st.columns(3)
filter_pet = col1.selectbox("Filter by Pet", ["All"] + pet_names)
filter_status = col2.selectbox("Filter by Status", ["All", "Pending", "Completed"])
filter_priority = col3.selectbox("Filter by Priority", ["All", "high", "medium", "low"])

all_tasks = scheduler.sort_by_time()
filtered_tasks = all_tasks

if filter_pet != "All":
    filtered_tasks = [t for t in filtered_tasks if t.pet_name == filter_pet]
if filter_status == "Pending":
    filtered_tasks = [t for t in filtered_tasks if not t.is_complete]
elif filter_status == "Completed":
    filtered_tasks = [t for t in filtered_tasks if t.is_complete]
if filter_priority != "All":
    filtered_tasks = [t for t in filtered_tasks if t.priority == filter_priority]

if not filtered_tasks:
    st.info("No tasks match your filters. Add a pet and some tasks to get started!")
else:
    priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    for task in filtered_tasks:
        status_label = "✅ Done" if task.is_complete else "⏳ Pending"
        icon = priority_icons.get(task.priority, "⚪")
        with st.expander(f"{icon} {task.time} — {task.title} ({task.pet_name})  [{status_label}]"):
            st.write(f"**Pet:** {task.pet_name}")
            st.write(f"**Category:** {task.category}")
            st.write(f"**Frequency:** {task.frequency}")
            st.write(f"**Priority:** {task.priority}")
            if task.description:
                st.write(f"**Notes:** {task.description}")
            if not task.is_complete:
                if st.button(f"Mark Complete", key=f"complete_{id(task)}"):
                    next_t = scheduler.mark_task_complete(task)
                    if next_t:
                        st.success(f"Done! Next '{task.title}' scheduled for {next_t.due_date}")
                    else:
                        st.success("Task marked complete!")
                    st.rerun()

# ── Pets Overview ─────────────────────────────────────────────────────────────
st.subheader("🐶 Pets Overview")
if owner.pets:
    cols = st.columns(min(len(owner.pets), 3))
    for i, pet in enumerate(owner.pets):
        with cols[i % 3]:
            pending_count = len(pet.get_pending_tasks())
            total_count = len(pet.tasks)
            st.metric(label=f"{pet.name} ({pet.species})", value=f"{pending_count} pending", delta=f"{total_count} total")
else:
    st.info("No pets added yet. Use the sidebar to add your first pet!")
