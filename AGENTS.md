# Project automation guidance

## Goal
Convert an SRS document into a Jira-ready backlog in a predictable, reviewable way.

## Backlog decomposition rules
1. Parse the SRS into features/capabilities first.
2. Create **Epics** for major capability groups or modules.
3. Create **Stories** for user-visible outcomes under each Epic.
4. Create **Tasks** for implementation/engineering work under each Story.
5. Create **Subtasks** only when a Task has clear, separable execution steps.

## Quality and consistency constraints
- **No duplicate tasks**: before adding an item, compare normalized title + intent against existing items.
- **Acceptance criteria required**: every Epic, Story, Task, and Subtask must include explicit acceptance criteria.
- **Unclear requirements**: if requirement intent, scope, or dependency is ambiguous, set status to `needs-review`.
- **AI provenance label**: every generated item must include label `ai-generated`.

## Jira creation order
1. Create Epics first.
2. Then create Stories/Tasks and link to parent Epic.
3. Then create Subtasks and link to parent Story/Task.

## Validation checklist before Jira creation
- Backlog JSON matches `backlog_schema.json`.
- Each item has: title, description, acceptance_criteria, labels.
- `ai-generated` is present in labels for all items.
- No duplicate titles within the same parent scope.
