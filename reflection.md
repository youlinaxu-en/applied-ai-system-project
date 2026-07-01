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
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
This tradeoff is reasonable because the app’s main purpose is to support responsible pet care. In this scenario, missing an important health-related task is worse than making the schedule slightly less convenient. The scheduler should therefore favor pet health and task urgency over perfect convenience.