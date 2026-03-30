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
Yes, the design evolved significantly during implementation based on practical needs. Major changes include: (1) Task was simplified from using datetime objects with `due_time` and `status` to using simple `time: str` (HH:MM format) and `is_complete: bool`, better suited for UI input and the app workflow. (2) Task now includes a `frequency` field ("once", "daily", "weekly") to natively support recurring tasks rather than relying on external scheduling logic. (3) The `pet` reference in Task changed from a Pet object to `pet_name: str` for simpler serialization and UI handling. (4) The entire ScheduledItem class was removed as unnecessary for the streaming app's task-list paradigm, reducing complexity. (5) Pet.needs was replaced with Pet.tasks to directly store the task list on each pet. (6) Scheduler.build_daily_schedule was replaced with utility methods like sort_by_time, filter_by_pet, detect_conflicts, and mark_task_complete, shifting from a complex scheduling algorithm to a flexible task management interface. These changes prioritized simplicity, UI-friendliness, and practical usability over theoretical completeness.
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

After starting with a complex scheduling engine, I realized the app didn't need automatic schedule generation—it needed a good task management system instead. The scheduler now tracks two key constraints: (1) Time, represented as a simple HH:MM string, which lets users see when tasks are due at a glance. (2) Priority level (low, medium, high), which helps users decide what to tackle first. I also kept the frequency field to handle recurring tasks automatically. Owner preferences (like daily availability) were removed because a pet owner using this app will manually pick their own schedule—the system doesn't mandate when things happen.

**b. Tradeoffs**

The biggest tradeoff is that the system doesn't automatically avoid time conflicts. If a user schedules a morning walk at 8 AM and a vet visit at 8 AM, both show up in the UI, but the system only warns about the collision—it depends on the user to resolve it. This simplifies the code significantly and actually fits the real world better: a pet owner knows their constraints (the vet appointment is non-negotiable), so imposing algorithmic constraints doesn't help. The app is a tool for planning, not a prescriptive scheduler.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI heavily throughout the project. In the design phase, AI helped me brainstorm the UML structure and validate that my classes covered the main requirements. When building the system, AI generated solid class skeletons, and I iterated from there. I asked for help debugging subtle issues like ensuring recurring tasks actually create the next instance, and AI caught mistakes in my logic quickly. The most helpful prompts were specific ones: "How should I handle recurring tasks that get marked complete?" worked better than vague ones like "Make the scheduler better." I also used AI to review my code for cleanliness and suggest refactorings—that caught unnecessary complexity I'd built in.

**b. Judgment and verification**

Early on, AI suggested building a full constraint-satisfaction solver for scheduling conflicts. I politely declined and asked for a simpler approach. I realized that over-engineering the conflict detection would bloat the code when a simple warning system (showing tasks at the same time) was enough. To verify this was the right call, I sketched out the user workflow: does an app user want the system to automatically shuffle their tasks around, or does the user want to see problems and fix them? The answer was obviously the latter. So I rejected the AI suggestion and went with simpler warnings instead. That decision made the whole codebase cleaner and more maintainable.

---

## 4. Testing and Verification

**a. What you tested**

I tested the core task management behaviors: adding/removing tasks from pets, filtering tasks by pet and status, sorting by time, and detecting time conflicts. I also verified that completing a recurring daily or weekly task correctly generates the next occurrence. These tests matter because they're the actual operations users will perform—if marking a task complete doesn't create the next one, the whole recurring system breaks. I also spot-checked edge cases like completing a "once-only" task (should return None, not generate a ghost next task).

**b. Confidence**

I'm pretty confident the core functionality works. The filtering and sorting are straightforward and hard to break. The task completion logic is tested and handles the three frequency types correctly. Where I'm less confident: I haven't fully tested the Streamlit integration yet—there could be unexpected issues when the UI feeds data into the system. Also, I haven't tested performance with large numbers of tasks (say, 500+), though for a single pet owner that's unlikely to be a real problem. If I had more time, I'd test: (1) What happens if someone edits a task's pet_name after creation? (2) Do recurring tasks handle leap days or DST transitions correctly? (3) Can the system handle multiple owners' data without cross-contamination (if we ever add that)?

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the decision to simplify the design based on real requirements. The original UML had a lot of structure that looked good on paper but didn't match what the app actually needed. Recognizing that and pivoting was the right call—now the system is clean, easy to understand, and actually useful. The Task and Pet dataclasses came out really well, and the idea of storing tasks directly on pets (instead of a central task list) makes the object model intuitive to work with.

**b. What you would improve**

I'd add proper validation and error handling. Right now, if someone tries to mark a task for a pet that doesn't exist, the system is too forgiving. I'd also add timestamps to track when tasks were created or modified—useful for debugging and for a more complete audit trail. The frequency system could be smarter: instead of just "daily" or "weekly," it could support things like "every 3 days" or "Mondays and Thursdays." That would need a different data model though. Finally, I'd refactor Scheduler.detect_conflicts to handle multi-owner scenarios if that ever becomes a requirement.

**c. Key takeaway**

The biggest lesson: let the requirements and the actual user workflow shape your design, not your initial diagram. I spent time designing a complex scheduler that the app didn't need. It was only when I built the Streamlit UI and saw how the user would interact with the system that I realized a simpler approach was better. Designing with AI is powerful, but the human has to stay critical and ask "does this actually serve the user?" rather than just implementing whatever the AI suggests. Good design is driven by constraints and real workflows, not by theoretical purity.
