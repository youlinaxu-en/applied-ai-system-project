from datetime import date, datetime

from pawpal_system import Owner, Pet, Task, TaskCategory, Priority, Scheduler


def at(hour: int, minute: int = 0) -> datetime:
    return datetime.combine(date.today(), datetime.min.time()).replace(hour=hour, minute=minute)


def main():
    owner = Owner(1, "Youlina", "youlinaxu@gmail.com")

    dog = Pet(1, "Biscuit", "dog", "Golden Retriever", age=3)
    cat = Pet(2, "Mochi", "cat", "Tabby", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(1, "Morning walk", TaskCategory.WALK, at(8, 0), Priority.MEDIUM))
    dog.add_task(Task(2, "Give medication", TaskCategory.MEDICATION, at(7, 0), Priority.CRITICAL))
    cat.add_task(Task(3, "Evening feeding", TaskCategory.FEEDING, at(18, 30), Priority.HIGH))

    scheduler = Scheduler()
    todays_tasks = scheduler.get_tasks_for_day(owner, date.today())

    print("=== Today's Schedule ===")
    for task in todays_tasks:
        time_str = task.scheduled_time.strftime("%I:%M %p")
        pet_name = task.pet.name if task.pet else "Unknown pet"
        print(f"{time_str} - {pet_name}: {task.description} [{task.priority.value}]")


if __name__ == "__main__":
    main()
