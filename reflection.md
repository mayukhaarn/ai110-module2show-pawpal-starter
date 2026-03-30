# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

Pet: A dataclass representing a pet's basic information (name, species, age, weight) and care needs, with methods to add/remove needs, retrieve care requirements, and generate a descriptive summary.

Task: A dataclass for individual pet care tasks, including details like title, duration, priority, and status, with methods to calculate a priority-based score, mark tasks as complete, check for overdue status, and estimate completion time.

ScheduledItem: A dataclass linking a task to a specific time slot, assigned owner, and optional notes, with methods to calculate duration, detect scheduling overlaps, and convert to a dictionary for display.

Owner: A class managing the pet owner's profile (name, email, preferences), their list of pets, and methods to add/remove pets, check ownership, and determine daily time availability based on preferences.

Scheduler: A class responsible for coordinating pet care planning, maintaining lists of tasks and pets for an owner, and providing methods to add/remove tasks, build priority-sorted daily schedules, score individual tasks, explain the generated plan, identify conflicts, and clear schedules.

- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
Yes, the design was refined to better incorporate constraints and preferences. Specifically, Task.compute_score was updated to factor in due_time proximity (adding a bonus for tasks due soon), and Scheduler.build_daily_schedule was modified to prevent scheduling overlapping tasks for the same pet, ensuring pets aren't double-booked.
- If yes, describe at least one change and why you made it.

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
