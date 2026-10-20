from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")

    cat = Pet("Mochi", "cat")
    dog = Pet("Biscuit", "dog")

    cat.add_task(
        Task(
            description="Evening medication",
            time=time(19, 0),
            frequency="daily",
            duration_minutes=5,
            priority="medium",
        )
    )
    dog.add_task(
        Task(
            description="Morning walk",
            time=time(8, 0),
            frequency="daily",
            duration_minutes=30,
            priority="high",
        )
    )
    cat.add_task(
        Task(
            description="Breakfast",
            time=time(8, 0),
            frequency="daily",
            duration_minutes=10,
            priority="high",
        )
    )

    owner.add_pet(cat)
    owner.add_pet(dog)
    scheduler = Scheduler(owner)
    task_pets = {task: pet for pet in owner.pets for task in pet.tasks}

    print("Today's Schedule")
    for task in scheduler.sort_by_time(scheduler.filter_tasks(completed=False)):
        pet = task_pets[task]
        print(
            f"{task.time:%H:%M} | {pet.name} ({pet.species}) | "
            f"{task.description} ({task.duration_minutes} min, "
            f"{task.priority} priority, {task.frequency})"
        )

    conflict_warnings = scheduler.get_conflict_warnings(date.today())
    if conflict_warnings:
        print("\nSchedule Warnings")
        for warning in conflict_warnings:
            print(f"WARNING: {warning}")

    print(f"\n{cat.name}'s Tasks")
    cat_tasks = scheduler.filter_tasks(pet_name=cat.name, completed=False)
    for task in scheduler.sort_by_time(cat_tasks):
        print(f"{task.time:%H:%M} | {task.description}")


if __name__ == "__main__":
    main()