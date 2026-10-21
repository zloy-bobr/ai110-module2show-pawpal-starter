# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I chose four classes for the system:

- `Task` represents one activity with a description, optional time, frequency, completion status, duration, and priority.
- `Pet` stores a pet's name and species, plus its tasks, and provides methods to add or remove tasks.
- `Owner` stores the owner's name and pets, manages the pet list, and provides `get_all_tasks()` to collect tasks across every pet.
- `Scheduler` uses an `Owner` to retrieve all tasks, organize pending tasks by time and priority, and mark an owner's task complete.

One owner can have multiple pets, and each pet can have multiple tasks. A scheduler belongs to one owner and accesses tasks through that owner's `get_all_tasks()` method, so it can work across multiple pets.

**b. Design changes**

The initial `CareTask` and `DailySchedule` draft was changed to `Task` and `Scheduler` to match the required responsibilities. The scheduler now receives an owner and gets tasks only through `Owner.get_all_tasks()`, rather than depending on one pet; it also filters, orders, and manages task completion. Task inputs validate non-empty descriptions and frequencies, positive durations, and supported priorities. Owner preferences are not modeled yet, so preference-based scheduling would need an additional design decision later.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers each task's scheduled time, duration, priority, recurrence date, completion status, and pet. For the generated schedule, time comes first, then priority and task description; tasks without a time appear last. Duration is used to detect overlaps, not to move tasks automatically. I prioritized time because care tasks may need to happen at a particular hour, then used priority to order tasks with the same time. Owner preferences are not represented in this version.

**b. Tradeoffs**

The scheduler reports overlapping tasks but does not automatically move or reschedule them. This keeps scheduling predictable and preserves the times the owner entered, while leaving the owner to decide which task should change when a conflict occurs.

---

## 3. AI Collaboration

**a. How you used AI**

I used the assistant to brainstorm the class model, draft code and tests, explain the scheduling behavior, and review the UML and README against the implementation. The most effective features were focused code generation, test suggestions, and review questions about concrete requirements such as multi-pet task retrieval and same-time sorting. Specific prompts with method names and expected behavior produced more useful results than broad requests to build the whole application.

Separate chat sessions for design, implementation, testing, and documentation helped keep each phase's goal clear. I could focus each session on a small deliverable, such as checking recurrence tests or updating the UML, without mixing it with unrelated UI or documentation questions. I still checked decisions against the code and the project requirements rather than treating each answer as authoritative.

**b. Judgment and verification**

The initial draft used `CareTask` and `DailySchedule`, but I changed those to `Task` and `Scheduler` to match the required responsibilities. The assistant pointed out that owner preferences were not modeled. I kept that feature out because the UI does not collect preferences and adding them would expand the design beyond the current scheduling requirements. Similarly, the scheduler reports conflicts but leaves rescheduling to the owner, keeping entered times unchanged. I verified the implementation with `python main.py` and `python -m pytest`; the demo showed tasks from two pets and the test suite passed all 13 tests.

---

## 4. Testing and Verification

**a. What you tested**

The tests cover task assignment, filtering by pet and completion status, case-insensitive pet-name filtering, recurrence dates, and schedule ordering by time and priority. They also check daily and weekly next occurrences, as-needed and repeated completion behavior, and conflict detection for overlapping tasks, including tasks at the same time and tasks that meet end-to-start. These checks matter because filtering, recurrence, and overlap errors could make a schedule omit care tasks, show them on the wrong date, or give the owner misleading warnings.

**b. Confidence**

I am reasonably confident in the core scheduler behavior: all 13 automated tests pass, and the terminal demo shows a schedule across two pets with a conflict warning. I would not call it exhaustive because the Streamlit interface is not covered by automated UI tests. Next I would test an owner with no pets or tasks, invalid task inputs, duplicate pet names, and tasks whose durations cross midnight. I would also clarify and test how as-needed tasks should appear on future dates.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the scheduler works across multiple pets through the owner's task collection method, while keeping task ownership clear. The same-time sorting and conflict warning make schedule behavior visible instead of silently changing the owner's plan.

**b. What you would improve**

In another iteration, I would add UI controls to edit and remove tasks, then consider optional owner preferences such as unavailable time windows. I would add automated tests for the Streamlit workflows and decide explicitly how to handle tasks that extend past midnight before changing the conflict algorithm.

**c. Key takeaway**

I learned that being the lead architect means defining the requirements and boundaries, choosing which tradeoffs fit the user, and verifying the result. AI made it faster to draft code and tests, but I still had to decide what belonged in the design, reject unnecessary complexity, and check that the implementation and documentation matched the actual behavior.
