from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    completed_on = date(2026, 10, 19)
    task = Task(
        "Morning walk",
        time=time(8, 30),
        duration_minutes=25,
        priority="high",
        recurrence_start=completed_on,
    )
    pet = Pet("Mochi", "cat", tasks=[task])
    owner = Owner("Jordan", pets=[pet])
    scheduler = Scheduler(owner)

    assert task.completed is False
    next_task = scheduler.mark_complete(task, today=completed_on)

    assert task.completed is True
    assert next_task is not None
    assert next_task is not task
    assert next_task.recurrence_start == completed_on + timedelta(days=1)
    assert next_task.description == task.description
    assert next_task.time == task.time
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.priority == task.priority
    assert next_task.completed is False
    assert next_task in pet.tasks


def test_weekly_completion_creates_next_occurrence_in_seven_days() -> None:
    completed_on = date(2026, 10, 19)
    task = Task("Grooming", frequency="weekly", recurrence_start=completed_on)
    pet = Pet("Mochi", "cat", tasks=[task])
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    next_task = scheduler.mark_complete(task, today=completed_on)

    assert next_task is not None
    assert next_task.frequency == "weekly"
    assert next_task.recurrence_start == completed_on + timedelta(days=7)


def test_as_needed_completion_does_not_create_an_occurrence() -> None:
    task = Task("Extra play", frequency="as needed")
    pet = Pet("Mochi", "cat", tasks=[task])
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    assert scheduler.mark_complete(task, today=date(2026, 10, 19)) is None
    assert task.completed is True
    assert pet.tasks == [task]


def test_completing_the_same_task_twice_does_not_duplicate_occurrences() -> None:
    task = Task("Breakfast")
    pet = Pet("Mochi", "cat", tasks=[task])
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    next_task = scheduler.mark_complete(task, today=date(2026, 10, 19))
    assert next_task is not None
    assert scheduler.mark_complete(task, today=date(2026, 10, 19)) is None
    assert pet.tasks == [task, next_task]


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "cat")
    initial_task_count = len(pet.tasks)

    pet.add_task(Task("Breakfast"))

    assert len(pet.tasks) == initial_task_count + 1


def test_filtering_by_pet_and_completion_status() -> None:
    pending_task = Task("Breakfast")
    completed_task = Task("Medication", completed=True)
    other_pet_task = Task("Walk")
    cat = Pet("Mochi", "cat", tasks=[pending_task, completed_task])
    dog = Pet("Biscuit", "dog", tasks=[other_pet_task])
    scheduler = Scheduler(Owner("Jordan", pets=[cat, dog]))

    assert scheduler.filter_tasks(pet=cat, completed=False) == [pending_task]
    assert scheduler.filter_tasks(completed=True) == [completed_task]


def test_filtering_by_pet_name_is_case_insensitive() -> None:
    cat_task = Task("Breakfast")
    dog_task = Task("Walk")
    cat = Pet("Mochi", "cat", tasks=[cat_task])
    dog = Pet("Biscuit", "dog", tasks=[dog_task])
    scheduler = Scheduler(Owner("Jordan", pets=[cat, dog]))

    assert scheduler.filter_tasks(pet_name="mochi") == [cat_task]


def test_tasks_are_due_according_to_frequency() -> None:
    start = date(2026, 10, 19)
    daily_task = Task("Feeding", recurrence_start=start)
    weekly_task = Task("Grooming", frequency="weekly", recurrence_start=start)
    as_needed_task = Task("Extra play", frequency="as needed", recurrence_start=start)

    assert daily_task.occurs_on(date(2026, 10, 20))
    assert weekly_task.occurs_on(date(2026, 10, 26))
    assert not weekly_task.occurs_on(date(2026, 10, 20))
    assert as_needed_task.occurs_on(date(2026, 10, 21))
    assert not weekly_task.occurs_on(date(2026, 10, 18))


def test_organize_tasks_sorts_by_time_then_priority() -> None:
    later_task = Task("Walk", time(9, 0), priority="high")
    low_priority_task = Task("Water", time(8, 0), priority="low")
    high_priority_task = Task("Feed", time(8, 0), priority="high")
    pet = Pet("Mochi", "cat", tasks=[later_task, low_priority_task, high_priority_task])
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    assert scheduler.organize_tasks() == [
        high_priority_task,
        low_priority_task,
        later_task,
    ]


def test_sort_by_time_uses_hh_mm_order_and_puts_unscheduled_last() -> None:
    evening_task = Task("Medication", time(19, 0))
    morning_task = Task("Breakfast", time(7, 0))
    unscheduled_task = Task("Play")
    pet = Pet("Mochi", "cat", tasks=[evening_task, unscheduled_task, morning_task])
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    assert scheduler.sort_by_time() == [morning_task, evening_task, unscheduled_task]


def test_organize_tasks_can_include_completed_tasks() -> None:
    pending_task = Task("Breakfast")
    completed_task = Task("Medication", completed=True)
    pet = Pet("Mochi", "cat", tasks=[pending_task, completed_task])
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    assert scheduler.organize_tasks() == [pending_task]
    assert scheduler.organize_tasks(include_completed=True) == [
        pending_task,
        completed_task,
    ]


def test_conflict_detection_reports_overlaps_not_back_to_back_tasks() -> None:
    day = date(2026, 10, 19)
    first_task = Task("First walk", time(8, 0), duration_minutes=30, recurrence_start=day)
    same_time_task = Task("Feeding", time(8, 0), duration_minutes=30, recurrence_start=day)
    overlapping_task = Task(
        "Medication", time(8, 15), duration_minutes=10, recurrence_start=day
    )
    back_to_back_task = Task(
        "Play", time(8, 30), duration_minutes=20, recurrence_start=day
    )
    cat = Pet("Mochi", "cat", tasks=[first_task, same_time_task])
    dog = Pet("Biscuit", "dog", tasks=[overlapping_task, back_to_back_task])
    scheduler = Scheduler(Owner("Jordan", pets=[cat, dog]))

    conflicts = scheduler.find_conflicts(day)

    assert len(conflicts) == 3
    assert (first_task, same_time_task) in conflicts
    assert (first_task, overlapping_task) in conflicts
    assert (same_time_task, overlapping_task) in conflicts


def test_conflict_warnings_are_readable_and_empty_when_no_conflict() -> None:
    day = date(2026, 10, 19)
    breakfast = Task("Breakfast", time(8, 0), duration_minutes=30, recurrence_start=day)
    walk = Task("Morning walk", time(8, 0), duration_minutes=30, recurrence_start=day)
    cat = Pet("Mochi", "cat", tasks=[breakfast])
    dog = Pet("Biscuit", "dog", tasks=[walk])
    scheduler = Scheduler(Owner("Jordan", pets=[cat, dog]))

    warnings = scheduler.get_conflict_warnings(day)

    assert warnings == [
        "Mochi's Breakfast at 08:00 overlaps with Biscuit's Morning walk at 08:00."
    ]
    assert scheduler.get_conflict_warnings(day, pet=cat) == []