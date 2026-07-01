from datetime import datetime, timedelta

from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task, TaskCategory, TaskStatus


def test_mark_done_changes_task_status():
    task = Task(1, "Morning walk", TaskCategory.WALK, datetime(2026, 7, 1, 8, 0), Priority.MEDIUM)
    assert task.status == TaskStatus.PENDING

    task.mark_done()

    assert task.status == TaskStatus.DONE


def test_adding_task_increases_pet_task_count():
    pet = Pet(1, "Biscuit", "dog", "Golden Retriever", age=3)
    assert len(pet.get_tasks()) == 0

    task = Task(1, "Give medication", TaskCategory.MEDICATION, datetime(2026, 7, 1, 7, 0), Priority.CRITICAL)
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner(1, "Youlina", "youlinaxu@gmail.com")
    pet = Pet(1, "Biscuit", "dog")
    owner.add_pet(pet)

    pet.add_task(Task(1, "Evening feeding", TaskCategory.FEEDING, datetime(2026, 7, 1, 18, 30), Priority.HIGH))
    pet.add_task(Task(2, "Give medication", TaskCategory.MEDICATION, datetime(2026, 7, 1, 7, 0), Priority.CRITICAL))
    pet.add_task(Task(3, "Morning walk", TaskCategory.WALK, datetime(2026, 7, 1, 8, 0), Priority.MEDIUM))

    ordered = Scheduler().sort_by_time(owner.get_all_tasks())

    assert [t.id for t in ordered] == [2, 3, 1]


def test_marking_daily_task_done_creates_task_for_next_day():
    owner = Owner(1, "Youlina", "youlinaxu@gmail.com")
    pet = Pet(1, "Biscuit", "dog")
    owner.add_pet(pet)

    task = Task(
        1,
        "Give daily pill",
        TaskCategory.MEDICATION,
        datetime(2026, 7, 1, 7, 0),
        Priority.CRITICAL,
        frequency=Frequency.DAILY,
    )
    pet.add_task(task)

    task.mark_done()

    new_tasks = [t for t in pet.get_tasks() if t.id != task.id]
    assert len(new_tasks) == 1
    next_task = new_tasks[0]
    assert next_task.status == TaskStatus.PENDING
    assert next_task.frequency == Frequency.DAILY
    assert next_task.scheduled_time == task.scheduled_time + timedelta(days=1)


def test_scheduler_flags_duplicate_time_across_pets():
    owner = Owner(1, "Youlina", "youlinaxu@gmail.com")
    dog = Pet(1, "Biscuit", "dog")
    cat = Pet(2, "Mochi", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(1, "Morning walk", TaskCategory.WALK, datetime(2026, 7, 1, 8, 0), Priority.MEDIUM))
    cat.add_task(Task(2, "Grooming session", TaskCategory.GROOMING, datetime(2026, 7, 1, 8, 0), Priority.LOW))

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Grooming session" in warnings[0]
