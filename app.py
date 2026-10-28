from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# Streamlit reruns this script on every interaction, so the Owner lives in session state.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="D'Jaine")
owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

st.divider()

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name, key="owner_name")

st.subheader("Pets")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if not pet_name.strip():
        st.warning("Please enter a pet name.")
    elif owner.get_pet(pet_name.strip()):
        st.warning(f"{pet_name.strip()} has already been added.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species))
        st.success(f"Added {pet_name.strip()} the {species}.")

if owner.pets:
    st.table([{"Pet": pet.name, "Species": pet.species} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for them.")
else:
    selected_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])

    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task description", value="Morning walk")
    with col2:
        task_time = st.time_input("Time", value=time(8, 0))

    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        if not task_title.strip():
            st.warning("Please enter a task description.")
        else:
            pet = owner.get_pet(selected_pet_name)
            pet.add_task(
                Task(
                    description=task_title.strip(),
                    time=task_time.strftime("%H:%M"),
                    duration_minutes=int(duration),
                    priority=priority,
                    frequency=frequency,
                )
            )
            st.success(f"Added '{task_title.strip()}' for {pet.name}.")

st.divider()

st.subheader("Today's Schedule")

# The completion control sits above the table so its handler runs before the table is drawn.
pending = [(pet, task) for pet, task in scheduler.get_todays_schedule() if not task.completed]
if pending:
    choice = st.selectbox(
        "Mark a task complete",
        range(len(pending)),
        format_func=lambda i: f"{pending[i][1].time}  {pending[i][1].description} ({pending[i][0].name})",
    )
    if st.button("Mark complete"):
        pet, task = pending[choice]
        tasks_before = len(pet.tasks)
        scheduler.mark_task_complete(pet, task)
        if len(pet.tasks) > tasks_before:
            next_task = pet.tasks[-1]
            st.success(
                f"Marked '{task.description}' complete. "
                f"Next {task.frequency} occurrence scheduled for {next_task.due_date}."
            )
        else:
            st.success(f"Marked '{task.description}' complete.")

for warning in scheduler.detect_conflicts():
    st.warning(f"{warning}. Consider moving one of these tasks to a different time.")

schedule = scheduler.get_todays_schedule()
if schedule:
    st.success(f"{len(schedule)} task(s) scheduled for today, sorted by time.")
    st.table(
        [
            {
                "Time": task.time,
                "Pet": pet.name,
                "Task": task.description,
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Done": "✅" if task.completed else "⬜",
            }
            for pet, task in schedule
        ]
    )
else:
    st.info("Nothing scheduled for today yet.")

st.divider()

st.subheader("All Tasks")
col1, col2 = st.columns(2)
with col1:
    pet_filter = st.selectbox("Filter by pet", ["All"] + [pet.name for pet in owner.pets])
with col2:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

filtered = scheduler.sort_by_time(
    scheduler.filter_tasks(
        pet_name=None if pet_filter == "All" else pet_filter,
        completed={"All": None, "Pending": False, "Completed": True}[status_filter],
    )
)
if filtered:
    st.table(
        [
            {
                "Date": str(task.due_date),
                "Time": task.time,
                "Pet": pet.name,
                "Task": task.description,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Done": "✅" if task.completed else "⬜",
            }
            for pet, task in filtered
        ]
    )
else:
    st.info("No tasks match these filters.")
