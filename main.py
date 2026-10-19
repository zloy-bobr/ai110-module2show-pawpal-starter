from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")

    cat = Pet("Mochi", "cat")
    dog = Pet("Biscuit", "dog")

    cat.add_task(
        Task(
            description="Breakfast",
            time=time(7, 0),
            frequency="daily",
            duration_minutes=10,
            priority="high",
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
            description="Evening medication",
            time=time(19, 0),
            frequency="daily",
            duration_minutes=5,
            priority="medium",
        )
    )

    owner.add_pet(cat)
    owner.add_pet(dog)
    scheduler = Scheduler(owner)
    task_pets = {task: pet for pet in owner.pets for task in pet.tasks}

    print("Today's Schedule")
    for task in scheduler.organize_tasks():
        pet = task_pets[task]
        print(
            f"{task.time:%H:%M} | {pet.name} ({pet.species}) | "
            f"{task.description} ({task.duration_minutes} min, "
            f"{task.priority} priority, {task.frequency})"
        )


if __name__ == "__main__":
    main()