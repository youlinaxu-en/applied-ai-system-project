from datetime import datetime

from pawpal_system import Pet, Priority, Task, TaskCategory, TaskStatus


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
