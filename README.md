# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

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

## Implementation Summary

`Task` stores an activity's description, time, frequency, recurrence start date, completion status, duration, and priority. Each `Pet` manages its own tasks, while `Owner` manages multiple pets and gathers their tasks with `get_all_tasks()`. `Scheduler` uses that owner-level method to filter by pet, completion status, and date; order tasks by time and priority; report overlapping timed tasks; and create the next daily or weekly task instance when one is completed. `timedelta` advances the next due date by one or seven days. In `app.py`, Streamlit keeps the `Owner` in session state and lets the user select a schedule date, pet, and task status. The `main.py` demo prints a readable terminal schedule, and tests cover task management and scheduling behavior.

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

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time`, `Scheduler.organize_tasks` | Sorts by zero-padded `HH:MM` (unscheduled last); organizer also uses priority and description. |
| Filtering | `Scheduler.filter_tasks` | Filters across the owner's pets by pet object or case-insensitive pet name, completion status, and date. |
| Conflict detection and warnings | `Scheduler.find_conflicts`, `Scheduler.get_conflict_warnings` | Finds duration overlaps between timed tasks, including across pets; touching end-to-start is not a conflict. Returns readable warning strings without raising when conflicts exist. |
| Recurring task dates | `Task.occurs_on` | Determines whether daily, weekly, and as-needed tasks are eligible on a selected date. |
| Next occurrence on completion | `Scheduler.mark_complete` | Marks the current task complete and creates a fresh daily or weekly task using a one- or seven-day `timedelta`; as-needed tasks do not repeat automatically. |

### Algorithm choices

Tasks are sorted by time first, with priority used to break same-time ties. Sorting only by priority could delay time-sensitive care, while sorting only by time would ignore urgency when times match. Recurrence uses a start date and a small set of frequencies rather than a full calendar-rule engine; this keeps behavior easy to explain, but does not model exceptions or custom intervals. Completing a daily or weekly task creates a new task for the next occurrence, while as-needed tasks remain one-off. Conflict detection sorts the day's timed tasks and scans active intervals. Compared with checking every possible pair, this is efficient on schedules with few overlaps; when many tasks overlap, the output itself can still contain a quadratic number of pairs.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
