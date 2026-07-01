# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
    Action added: Walks, Feeding, Meds, Enrichment, Grooming, Cleaning, Behavior Record, Health Check.

- Consider constraints (time available, priority, owner preferences)
    The system should detect conflicts with existing plans and reschedule flexible tasks when possible.
    If a task is not marked as Done before the due time, the system should keep it as Pending or mark it as Overdue and send a reminder to the owner.
    The system should consider each pet's species, breed, age, health conditions, medication schedule, and special care requirements.
    Each pet may have a profile page containing photos, descriptions, breed information, age, gender, sterilization status, personality, and public reactions from other users.
               
- Produce a daily plan and explain why it chose that plan
    Generate daily care plans based on owner availability, task priority, pet health needs, and owner preferences. This will help owner take control of their pets, especially when owner is not at home.

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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
=== Today's Schedule ===
07:00 AM - Biscuit: Give medication [critical]
06:30 PM - Mochi: Evening feeding [high]
08:00 AM - Biscuit: Morning walk [medium]
## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The suite in `tests/test_pawpal.py` covers:

- Task completion — `Task.mark_done()` transitions a task from `PENDING` to `DONE`.
- Pet task tracking — `Pet.add_task()` correctly appends the new task to that pet's task list.
- Sorting correctness — `Scheduler.sort_by_time()` returns tasks added out of order back in chronological order.
- Recurrence logic — completing a DAILY task automatically creates a new `PENDING` task for the next day (`scheduled_time + timedelta(days=1)`) instead of losing the recurring reminder.
- Conflict detection — `Scheduler.detect_conflicts()` flags two different pets' tasks scheduled at the same time.

Sample output from a successful run:

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.0, pluggy-1.6.0
rootdir: c:\Users\www33\OneDrive\桌面\Class\ai110-module2show-pawpal-starter
collected 5 items

tests\test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.01s ==============================
```

## 📐 Smarter Scheduling

### Sorting

- `Scheduler.sort_by_time(tasks)` — pure chronological sort (tie-broken by priority). Gives an agenda-style, time-ordered view of a task list.
- `Scheduler.sort_by_priority(tasks)` — priority first (CRITICAL → LOW), then time, then category urgency (medication/health checks outrank routine care at equal priority), then duration. This is what `Scheduler.get_tasks_for_day()` uses to build the daily plan.

### Filtering

- `Scheduler.filter_tasks(owner, pet_id=None, pet_name=None, status=None)` — filter an owner's tasks by pet (id or name), by completion status (`PENDING`/`DONE`/`OVERDUE`/`MISSED`), or any combination of both.
- `Pet.get_tasks_by_status(status)` — the same status filter scoped to a single pet.

### Conflict detection

Two intentionally separate layers:

- `Pet.add_task(task)` / `Task.reschedule(new_time)` (backed by `Pet.find_conflicts`) — a hard guard for one pet's own calendar. If a new or rescheduled task's time window overlaps another active task *for that same pet*, it raises `SchedulingConflictError` instead of silently double-booking.
- `Scheduler.detect_conflicts(owner)` — a lightweight, non-raising sweep across *all* of an owner's pets. Since one owner can't be in two places at once, this also catches two different pets' tasks landing at overlapping times, returning plain warning strings instead of an exception.

### Recurring tasks

- `Task.occurs_on(day)` — for a still-pending DAILY/WEEKLY task, reports whether it should appear on a given day without duplicating it into stored copies.
- `Task.mark_done()`, via `Task._spawn_next_occurrence()` — once a DAILY/WEEKLY task is completed, a new `Task` instance is automatically created for the next occurrence (`scheduled_time + timedelta(days=1)` or `+ timedelta(weeks=1)`). The completed task becomes a closed historical record and the new instance starts `PENDING`.
- `Owner.next_task_id()` — hands out a collision-free id for auto-spawned tasks (also used by the Streamlit UI for manually-added ones, so both paths share one id source).
- `Owner.get_tasks_for_date(day)` / `Scheduler.get_tasks_for_day(owner, day)` — combine both mechanisms: exact-date lookup for one-off tasks, plus `occurs_on` expansion for still-open recurring ones.

## 📸 Demo Walkthrough

### UI features

The Streamlit app (`app.py`) lets a user:

- Enter an owner name, which persists across reruns via `st.session_state`.
- Add one or more pets (name + species).
- Schedule a task for a chosen pet — title, category, priority, duration, and time — which appears immediately in a running table of every task across all pets (pet, time, priority, status).
- Generate today's schedule with one click, producing a priority-ordered plan for every task due that day.

### Example workflow

Add a pet → schedule a task → view today's schedule:

1. Enter an owner name and click Add pet for "Biscuit" (dog).
2. Under Schedule a Task, select Biscuit, enter "Morning walk" (category: walk, priority: medium, 8:00 AM), and click Add task.
3. Click **Generate schedule** — "Morning walk" appears under Today's Schedule at 08:00 AM.

### Key Scheduler behaviors

The Streamlit form covers adding tasks and a priority-sorted daily plan; the rest of the `Scheduler`/`Task` logic is exercised end-to-end in `main.py` rather than the UI:

- Conflict warnings — `Scheduler.detect_conflicts()` flags two different pets' tasks landing at the same time (e.g., Biscuit's walk and Mochi's grooming, both at 8:00 AM) without raising an error.
- Sorting — `Scheduler.get_tasks_for_day()` sorts by priority (critical/health tasks first), while `Scheduler.sort_by_time()` gives a pure chronological view of the same tasks.
- Filtering — `Scheduler.filter_tasks()` narrows the list down to just pending tasks, or just one pet's tasks, or both at once.
- Recurring auto-rollover — completing a DAILY task (Biscuit's medication) automatically spawns a new `PENDING` task for the next day instead of losing the reminder.

### Sample CLI output (`python main.py`)

```
=== Conflict Warnings ===
[!] Conflict: 'Morning walk' (Biscuit) at 08:00 AM overlaps with 'Grooming session' (Mochi) at 08:00 AM

=== Today's Schedule (by priority) ===
07:00 AM - Biscuit: Give medication [critical] (pending)
06:30 PM - Mochi: Evening feeding [high] (pending)
08:00 AM - Biscuit: Morning walk [medium] (pending)
08:00 AM - Mochi: Grooming session [medium] (pending)
09:30 AM - Biscuit: Enrichment play [low] (pending)
12:00 PM - Mochi: Litter box cleaning [low] (pending)

=== Sorted by Time ===
07:00 AM - Biscuit: Give medication [critical] (pending)
08:00 AM - Biscuit: Morning walk [medium] (pending)
08:00 AM - Mochi: Grooming session [medium] (pending)
09:30 AM - Biscuit: Enrichment play [low] (pending)
12:00 PM - Mochi: Litter box cleaning [low] (pending)
06:30 PM - Mochi: Evening feeding [high] (pending)

=== Filter: Pending Tasks Only ===
08:00 AM - Biscuit: Morning walk [medium] (pending)
09:30 AM - Biscuit: Enrichment play [low] (pending)
07:00 AM - Biscuit: Give medication [critical] (pending)
12:00 PM - Mochi: Litter box cleaning [low] (pending)
06:30 PM - Mochi: Evening feeding [high] (pending)
08:00 AM - Mochi: Grooming session [medium] (pending)

=== Filter: Biscuit's Tasks Only ===
08:00 AM - Biscuit: Morning walk [medium] (pending)
07:00 AM - Biscuit: Give medication [critical] (done)
09:30 AM - Biscuit: Enrichment play [low] (pending)
07:00 AM - Biscuit: Give medication [critical] (pending)

=== Recurring Auto-Rollover: Biscuit's Medication Tasks ===
  id=2 due=07/01 07:00 AM status=done
  id=7 due=07/02 07:00 AM status=pending
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
