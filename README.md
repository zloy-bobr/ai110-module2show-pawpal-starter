# PawPal+ Pet Care Scheduler

PawPal+ is a Streamlit app for managing pets' care tasks and generating a date-specific schedule. It supports multiple pets per owner and displays task times, priorities, durations, recurrence, and completion status.

## Features

- **Owner, pet, and task management:** Set the owner name, add pets, and create tasks with a time, duration, priority, and frequency in [`app.py`](app.py). The `Task`, `Pet`, and `Owner` models and their validation are implemented in [`pawpal_system.py`](pawpal_system.py).
- **Filtered schedules:** Choose a date, one pet or all pets, and pending, completed, or all tasks. The UI uses `Scheduler.organize_tasks()` and displays the results in a table.
- **Sorting:** Schedule results are ordered by time, then priority, then task description; tasks without a time appear last. `Scheduler.sort_by_time()` also provides chronological ordering.
- **Recurrence:** Daily tasks recur each day; weekly tasks recur every seven days from their start date. As-needed tasks are eligible on dates from their start date but do not automatically create a new task when completed.
- **Conflict warnings:** `Scheduler.find_conflicts()` detects overlaps between pending, timed tasks using their durations. It can report conflicts across pets; tasks that meet end-to-start are not considered overlapping. The UI displays warnings without changing task times.
- **Completion tracking:** Completing a daily or weekly task marks it complete and adds its next occurrence. Completing an as-needed task does not create another occurrence.
- **Input validation:** Tasks require a non-empty description, a positive duration, and supported frequency and priority values.

The scheduler does not currently model owner preferences or automatically resolve conflicts; it reports overlaps for the owner to address.

## Setup and Run

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start the Streamlit app:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Run the terminal demonstration with:

```bash
python main.py
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests cover task and pet management, task filtering, chronological and priority sorting, daily and weekly recurrence, completion behavior, and overlapping-task conflict warnings.

Test output:

```text
tests\test_pawpal.py .............                                       [100%]

============================= 13 passed in 0.07s ==============================
```

**Confidence Level:** 4/5 stars. The suite verifies the main scheduling and recurrence behaviors, including important edge cases, but it does not exhaustively test every input combination or the Streamlit interface.

## Demo Walkthrough

### Main UI

The app keeps the owner and pet data in Streamlit session state. Enter or update the owner name, add pets by name and species, and select a pet to add care tasks. Each task has a description, time, duration, priority, and frequency. The selected pet's task list shows its schedule details and completion status. Use the completion control to mark a pending task complete; daily and weekly tasks create their next occurrence automatically.

### Example Workflow

1. Start the app with `python -m streamlit run app.py`.
2. Add a pet, such as Mochi the cat, then select Mochi.
3. Add a task such as Breakfast at 08:00, with a duration and priority.
4. Add another pet, such as Biscuit the dog, and create a Morning walk also scheduled for 08:00.
5. In **Build Schedule**, select today's date, choose **All pets** and **Pending**, then generate the schedule.

The generated schedule is sorted by time, then priority and task description, and displayed with each task's pet, duration, frequency, and completion status. Because the example tasks overlap, the app shows a conflict warning. Change the date, pet filter, or status filter to view a different schedule.

### Terminal Demo

Run `python main.py` to see the multi-pet schedule and same-time conflict warning:

```text
Today's Schedule
08:00 | Mochi (cat) | Breakfast (10 min, high priority, daily)
08:00 | Biscuit (dog) | Morning walk (30 min, high priority, daily)
19:00 | Mochi (cat) | Evening medication (5 min, medium priority, daily)

Schedule Warnings
WARNING: Mochi's Breakfast at 08:00 overlaps with Biscuit's Morning walk at 08:00.

Mochi's Tasks
08:00 | Breakfast
19:00 | Evening medication
```
