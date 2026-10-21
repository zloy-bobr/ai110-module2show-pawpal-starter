from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.divider()

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name, key="owner_name")

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if not pet_name.strip():
        st.error("Enter a pet name before adding the pet.")
    else:
        try:
            owner.add_pet(Pet(pet_name.strip(), species))
        except ValueError as error:
            st.error(str(error))
        else:
            st.success(f"Added {pet_name.strip()}.")

if not owner.pets:
    st.info("Add a pet before creating care tasks.")
else:
    selected_pet_index = st.selectbox(
        "Choose a pet",
        range(len(owner.pets)),
        format_func=lambda index: (
            f"{owner.pets[index].name} ({owner.pets[index].species})"
        ),
        key="selected_pet_index",
    )
    selected_pet = owner.pets[selected_pet_index]

    st.subheader(f"Care tasks for {selected_pet.name}")
    with st.form("add_task_form", clear_on_submit=True):
        task_description = st.text_input("Task description", value="Morning walk")
        task_time = st.time_input("Task time", value=time(8, 0))
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col3:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        add_task = st.form_submit_button("Add task")

    if add_task:
        try:
            selected_pet.add_task(
                Task(
                    description=task_description,
                    time=task_time,
                    frequency=frequency,
                    duration_minutes=int(duration),
                    priority=priority,
                )
            )
        except ValueError as error:
            st.error(str(error))
        else:
            st.success(f"Added task for {selected_pet.name}.")

    if selected_pet.tasks:
        st.table(
            [
                {
                    "Task": task.description,
                    "Time": task.time.strftime("%H:%M") if task.time else "Any time",
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Completed": task.completed,
                }
                for task in selected_pet.tasks
            ]
        )
    else:
        st.info("No tasks for this pet yet.")

    pending_pet_tasks = [task for task in selected_pet.tasks if not task.completed]
    if pending_pet_tasks:
        with st.form(f"complete_task_form_{selected_pet_index}"):
            task_to_complete_index = st.selectbox(
                "Task to complete",
                range(len(pending_pet_tasks)),
                format_func=lambda index: pending_pet_tasks[index].description,
            )
            mark_task_complete = st.form_submit_button("Mark task complete")

        if mark_task_complete:
            next_task = Scheduler(owner).mark_complete(
                pending_pet_tasks[task_to_complete_index]
            )
            if next_task is None:
                st.success("Task marked complete.")
            else:
                st.success(
                    "Task marked complete. Next occurrence: "
                    f"{next_task.recurrence_start:%Y-%m-%d}."
                )

st.divider()

st.subheader("Build Schedule")
schedule_date = st.date_input("Schedule date", value=date.today())
pet_filter_index = st.selectbox(
    "Pet filter",
    [-1, *range(len(owner.pets))],
    format_func=lambda index: (
        "All pets"
        if index == -1
        else f"{owner.pets[index].name} ({owner.pets[index].species})"
    ),
    key="schedule_pet_filter",
)
task_status = st.selectbox("Task status", ["Pending", "Completed", "All"])

if st.button("Generate schedule"):
    schedule_pet = owner.pets[pet_filter_index] if pet_filter_index >= 0 else None
    completed_filter = {"Pending": False, "Completed": True, "All": None}[task_status]
    scheduler = Scheduler(owner)
    scheduled_tasks = scheduler.organize_tasks(
        include_completed=task_status == "All",
        pet=schedule_pet,
        on_date=schedule_date,
        completed=completed_filter,
    )
    if not scheduled_tasks:
        st.info("No tasks match these schedule filters.")
    else:
        task_pets = {
            task: pet for pet in owner.pets for task in pet.tasks
        }
        for warning in scheduler.get_conflict_warnings(
            schedule_date,
            pet=schedule_pet,
        ):
            st.warning(warning)
        st.table(
            [
                {
                    "Time": task.time.strftime("%H:%M") if task.time else "Any time",
                    "Pet": f"{task_pets[task].name} ({task_pets[task].species})",
                    "Task": task.description,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Completed": "Yes" if task.completed else "No",
                }
                for task in scheduled_tasks
            ]
        )
