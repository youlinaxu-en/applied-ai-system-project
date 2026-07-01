# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  My initial UML design focused on a pet care scheduling application with optional social features. The main goal was to allow an owner to enter pet information, create care tasks, and generate a daily plan based on time constraints and task priority.  
- What classes did you include, and what responsibilities did you assign to each?
The core classes I included were:

Class	                            Responsibility
Owner	                            Stores the user’s basic information, preferences, and owned pets.
Pet	                                Stores each pet’s profile information, such as name,    species, breed, age, gender, and personality.
HealthProfile	                    Stores long-term health information, such as allergies, medication needs, vaccination status, and special care instructions.
PetStatus	                        Records real-time or periodic status updates, such as mood, activity level, appetite, sleep, and abnormal signs.
CareTask	                        Represents a pet care task, such as feeding, walking, medication, grooming, or health checks.
AvailabilitySlot	                Represents the owner’s available time periods for completing pet care tasks.
DailyPlan	                        Stores the generated daily schedule and explanation for the plan.
ScheduledTask	                    Represents a CareTask after it has been assigned a specific start and end time.
CarePlanService	                    Handles the scheduling logic, including sorting tasks, checking conflicts, fitting tasks into available time, and generating explanations.
Reminder	                        Sends reminders when a task is due, pending, or overdue.
TaskService	                        Handles adding, editing, deleting, and retrieving tasks.

**b. Design changes**

- Did your design change during implementation?
    Yes, the design changed during implementation.

    

- If yes, describe at least one change and why you made it.
    One major change was adding a separate ScheduledTask class instead of letting DailyPlan directly contain CareTask objects.

    At first, I planned to let DailyPlan store a list of care tasks directly. However, this was not detailed enough because a task itself only describes what needs to be done, such as:

    Feed the dog
    Duration: 10 minutes
    Priority: High

    After scheduling, the system also needs to store when the task will happen:

    8:00 AM - 8:10 AM
    Feed the dog
    Reason: high-priority feeding task

    Because of this, I added ScheduledTask to store the scheduled start time, scheduled end time, and explanation for why the task was placed there.

    This change made the design clearer because:

    CareTask represents the original task.
    ScheduledTask represents the planned version of that task.
    DailyPlan contains scheduled tasks, not raw tasks.

    Another change was separating CarePlanService from DailyPlan. Originally, DailyPlan could have handled plan generation, but that would make the class responsible for both storing data and generating schedules. I moved the scheduling logic into CarePlanService so that DailyPlan only stores and displays the result.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
   

Constraint	        How it affects scheduling
Owner availability	Tasks should only be scheduled during time slots when the owner is available.
Task duration	    The scheduler must check whether a task can fit inside an available time slot.
Task priority	    Higher-priority tasks should be scheduled before lower-priority tasks.
Due time	        Tasks that are due sooner should be placed earlier when possible.
Pet health needs	Medication or health-related tasks should receive higher importance.
Owner preferences	Preferred time windows can influence where flexible tasks are placed.
Conflict detection	The scheduler should avoid overlapping tasks or placing tasks during unavailable times.

The most important constraints are availability, priority, and health-related urgency.

- How did you decide which constraints mattered most?
The most important constraints are availability, priority, and health-related urgency.

I decided these mattered most because the app is designed for pet care, not just general task management. Some pet care tasks are flexible, such as grooming or enrichment, but others are time-sensitive, such as medication or feeding. If the scheduler ignores priority or health needs, the generated plan may be convenient but unsafe or unrealistic.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

For example, a high-priority medication task may need to be scheduled during a less convenient time slot because it is time-sensitive. A lower-priority task, such as grooming or enrichment, may be delayed or moved to another available slot.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable because the app’s main purpose is to support responsible pet care. In this scenario, missing an important health-related task is worse than making the schedule slightly less convenient. The scheduler should therefore favor pet health and task urgency over perfect convenience.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
 It gives more special function but unnecessay suggestions, but not much useful in this assignment.

- How did you evaluate or verify what the AI suggested?
Ask a another AI assistant for its opinions.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested five core scheduler behaviors directly with pytest (`tests/test_pawpal.py`):

- `Task.mark_done()` flips a task's status from PENDING to DONE.
- `Pet.add_task()` correctly grows a pet's task list.
- `Scheduler.sort_by_time()` returns tasks added out of order back in chronological order.
- Marking a DAILY task done automatically creates exactly one new PENDING task scheduled exactly one day later.
- `Scheduler.detect_conflicts()` flags two different pets' tasks scheduled at the same time.

- Why were these tests important?

Beyond the pytest suite, I also verified behaviors manually while building each feature, because the riskiest bugs in this project weren't in simple "happy path" logic — they were in how features interacted:

- Calling `mark_done()` twice on the same recurring task must not spawn two next-occurrence tasks.
- Once a recurring task is marked done, it must not keep showing up alongside its newly spawned successor on the following day (an on-demand display rule and an auto-spawn rule can each look correct alone and still double-count together).
- The Streamlit app's own task-id counter had to be reconciled with the scheduler's auto-generated ids for recurring rollovers, so the two id sources couldn't collide.

These tests mattered because a scheduler that "looks right" in a one-off manual run can still have a latent bug that only shows up once a task recurs, gets rescheduled, or gets completed more than once.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I'm fairly confident in the paths that are covered by automated tests and by the `main.py` walkthrough — sorting, filtering, one-off conflict detection, and DAILY recurrence rollover all behave as expected and are exercised by both pytest and printed CLI output. I'm less confident about a few corners that only got manual, not automated, verification:

- WEEKLY recurrence rollover uses the same code path as DAILY but isn't covered by its own automated test yet.
- The overdue-detection heap (`Owner.pull_newly_overdue`) has lazy-deletion logic for stale entries left behind after a reschedule; that path has no dedicated test.
- I haven't verified what happens if a recurring task is rescheduled *and* later marked done — each behavior is tested on its own, not in combination.

- What edge cases would you test next if you had more time?

Marking a task done when it has no pet attached (should not crash and should not try to spawn a successor), rescheduling a task into a slot that only conflicts with an already-completed task (should be allowed, since completed tasks are excluded from conflict checks), and a WEEKLY rollover test with the same rigor as the DAILY one.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with keeping conflict handling as two separate, simple mechanisms instead of one complicated one: a hard `SchedulingConflictError` guard scoped to a single pet's own calendar, and a separate, non-raising `Scheduler.detect_conflicts()` sweep for conflicts across different pets. Neither method had to know about the other's job, which kept each one easy to reason about on its own.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd unify how "done-ness" is tracked for recurring tasks. Right now, completing a DAILY/WEEKLY task creates a brand-new `Task` object for the next occurrence, which works but means a pet's task list grows by one row per occurrence forever, with no archiving. A cleaner design would track completion per occurrence date on a single recurring `Task` instead of spawning a new object every time it's completed.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest lesson was that AI-suggested code can be individually correct and still combine into a bug. The on-demand recurring-task display logic and the auto-spawn-next-occurrence logic were each right in isolation, but together they would double-count a task on the day after it was completed unless I explicitly reconciled them. Writing my own small verification scripts after each change — instead of trusting that "it compiles and the demo prints the right thing" meant it was correct — is what caught that.