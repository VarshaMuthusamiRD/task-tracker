# Changelog
 
## Unreleased

### Added
- `/refactor` and `/review` slash commands for guided refactoring and code review workflows.
- Tests covering `completion_rate` rounding behavior and malformed task input.
- `CLAUDE.md` documenting project commands, structure, and conventions.
- `session-rules.md` documenting session conventions.
- Tests covering `completion_rate` edge cases (all-done, mixed, empty).
- Tests covering `due_date` validation and default behavior.
- Optional `due_date` field on `TaskStore.add`, validated as ISO format.
- `TaskStore.by_tag` to look up tasks by tag.
- Initial task store, reports module, and test suite.

### Changed
- Demo output now shows each task's due date.

### Fixed
- `add_tag` now raises `KeyError` for an unknown `task_id` instead of failing silently.
- `completion_rate` is now computed against the total number of tasks, not just the outstanding count.
- Each task now gets its own tags list instead of sharing one mutable default list across all tasks.
- `all()` now returns a copy of the task list instead of the live internal list.
- `set_status` now guards against a missing task instead of assuming `find()` succeeds.
