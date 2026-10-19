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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

I used an AI coding assistant to brainstorm the class model, draft the Python classes, create the terminal demo, and write focused tests. I asked it to review the class relationships and later to verify that the scheduler gathered tasks through the owner's `get_all_tasks()` method so it would work across multiple pets. Specific prompts about expected behavior and required method names were more useful than asking for a broad implementation.

**b. Judgment and verification**

The initial design used `CareTask` and `DailySchedule`, but the project requirements called for `Task` and `Scheduler`, so I changed the model to match those responsibilities. The AI review also noted that owner preferences are not represented; I left them out for this version because the requested implementation focuses on multi-pet task retrieval and the current UI does not collect preferences. I verified the result by running `python main.py` and `python -m pytest`; the demo printed tasks from two pets, and both tests passed, including the completion-status test.

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
