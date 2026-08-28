# Refactor Notes: TaskStore lookup/update consolidation

## Before

`set_status()` and `add_tag()` each independently performed task lookup and missing-ID
handling:

```python
def set_status(self, task_id, status):
    task = self.find(task_id)
    if task is None:
        raise KeyError(task_id)
    task["status"] = status
    return task

def add_tag(self, task_id, tag):
    task = self.find(task_id)
    if task is None:
        raise KeyError(task_id)
    task["tags"].append(tag)
    return task
```

This duplicated control flow meant the "what does a missing task mean here" decision was
made in two places instead of one. Any future change to that behavior (e.g. the error
type, or what counts as "missing") would have had to be made twice, with no guarantee the
two copies would stay in sync.

## After

A private helper, `_get_or_raise(task_id)`, was introduced. It wraps the existing `find`
lookup and raises `KeyError(task_id)` on a miss, returning the task otherwise.
`set_status` and `add_tag` now call this helper instead of repeating the check:

```python
def _get_or_raise(self, task_id):
    task = self.find(task_id)
    if task is None:
        raise KeyError(task_id)
    return task

def set_status(self, task_id, status):
    task = self._get_or_raise(task_id)
    task["status"] = status
    return task

def add_tag(self, task_id, tag):
    task = self._get_or_raise(task_id)
    task["tags"].append(tag)
    return task
```

`find()` itself is untouched — it still returns `None` on a miss, per this repo's
convention that lookups don't raise. `all()`, `by_tag()`, and `add()` are untouched.

## Why

The duplicated lookup logic was consolidated to give the missing-task behaviour a single
implementation point while preserving the existing public API and error behaviour. Both
methods previously encoded the same policy — "no task with this id is a `KeyError`" —
independently; consolidating it means that policy now has one place to change, one place
to test, and one place that can be gotten wrong, rather than two that could silently
drift apart over time. The refactor was scoped deliberately narrowly: no public
signatures, task structure, validation, or test files were touched, so the change is
behavior-preserving by construction rather than by verification alone.

## Evidence

- Tests before: 20/20 passing
- Tests after: 20/20 passing
- Existing tests modified: 0
- Behaviour changes: none
