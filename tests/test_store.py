import unittest
 
from tasks.store import TaskStore
 
 
class TestTaskStore(unittest.TestCase):
 
    def test_add_assigns_sequential_ids(self):
        store = TaskStore()
        first = store.add("Write the spec")
        second = store.add("Review the spec")
        self.assertEqual(first["id"], 1)
        self.assertEqual(second["id"], 2)
 
    def test_find_returns_the_matching_task(self):
        store = TaskStore()
        store.add("Write the spec")
        found = store.find(1)
        self.assertEqual(found["title"], "Write the spec")
 
    def test_set_status_updates_an_existing_task(self):
        store = TaskStore()
        store.add("Write the spec")
        store.set_status(1, "done")
        self.assertEqual(store.find(1)["status"], "done")
 
    def test_set_status_rejects_an_unknown_id(self):
        store = TaskStore()
        store.add("Write the spec")
        with self.assertRaises(KeyError):
            store.set_status(99, "done")
 
    def test_set_status_fails_cleanly_for_an_unknown_id(self):
        store = TaskStore()
        store.add("Write the spec")
        try:
            store.set_status(99, "done")
        except KeyError:
            return
        except TypeError:
            self.fail(
                "set_status(99, ...) raised TypeError instead of KeyError: "
                "it dereferences find()'s None result without checking for it"
            )
        self.fail("set_status(99, ...) did not raise for an unknown id")

    def test_tags_are_not_shared_between_tasks(self):
        store = TaskStore()
        store.add("Write the spec")
        store.add("Review the spec")
        store.add_tag(1, "urgent")
        self.assertEqual(store.find(2)["tags"], [])
 
    def test_all_returns_a_snapshot(self):
        store = TaskStore()
        store.add("Write the spec")
        snapshot = store.all()
        store.add("Review the spec")
        self.assertEqual(len(snapshot), 1)

    def test_by_tag_returns_only_tasks_with_that_tag(self):
        store = TaskStore()
        store.add("Write the spec")
        store.add("Review the spec")
        store.add_tag(1, "urgent")
        store.add_tag(2, "later")
        matches = store.by_tag("urgent")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["title"], "Write the spec")

    def test_by_tag_returns_multiple_matching_tasks(self):
        store = TaskStore()
        store.add("Write the spec")
        store.add("Review the spec")
        store.add_tag(1, "urgent")
        store.add_tag(2, "urgent")
        matches = store.by_tag("urgent")
        self.assertEqual([t["id"] for t in matches], [1, 2])

    def test_by_tag_returns_empty_list_when_no_task_has_the_tag(self):
        store = TaskStore()
        store.add("Write the spec")
        self.assertEqual(store.by_tag("urgent"), [])

    def test_add_accepts_a_valid_due_date(self):
        store = TaskStore()
        task = store.add("Write the spec", due_date="2026-09-01")
        self.assertEqual(task["due_date"], "2026-09-01")

    def test_add_defaults_due_date_to_none(self):
        store = TaskStore()
        task = store.add("Write the spec")
        self.assertIsNone(task["due_date"])

    def test_add_rejects_an_invalid_due_date(self):
        store = TaskStore()
        with self.assertRaises(ValueError):
            store.add("Write the spec", due_date="not-a-date")

    def test_add_rejects_a_non_iso_due_date_format(self):
        store = TaskStore()
        with self.assertRaises(ValueError):
            store.add("Write the spec", due_date="09/01/2026")


if __name__ == "__main__":
    unittest.main()
