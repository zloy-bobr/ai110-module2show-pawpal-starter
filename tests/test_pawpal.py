from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Morning walk")
    pet = Pet("Mochi", "cat", tasks=[task])
    owner = Owner("Jordan", pets=[pet])
    scheduler = Scheduler(owner)

    assert task.completed is False
    scheduler.mark_complete(task)
    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "cat")
    initial_task_count = len(pet.tasks)

    pet.add_task(Task("Breakfast"))

    assert len(pet.tasks) == initial_task_count + 1