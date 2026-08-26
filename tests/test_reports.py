import unittest

from tasks.reports import completion_rate


class TestCompletionRate(unittest.TestCase):

    def test_all_tasks_done_is_100_percent(self):
        tasks = [{"status": "done"}, {"status": "done"}]
        self.assertEqual(completion_rate(tasks), 100.0)

    def test_mixed_statuses_is_the_share_that_is_done(self):
        tasks = [{"status": "done"}, {"status": "pending"}]
        self.assertEqual(completion_rate(tasks), 50.0)

    def test_empty_list_is_0_percent(self):
        self.assertEqual(completion_rate([]), 0.0)

    def test_rounds_to_one_decimal_place(self):
        tasks = [
            {"status": "done"},
            {"status": "pending"},
            {"status": "pending"},
        ]
        self.assertEqual(completion_rate(tasks), 33.3)

    def test_task_missing_status_key_raises_key_error(self):
        tasks = [{"status": "done"}, {"title": "no status field"}]
        with self.assertRaises(KeyError):
            completion_rate(tasks)

    def test_non_dict_task_raises_type_error(self):
        tasks = ["not-a-task-dict"]
        with self.assertRaises(TypeError):
            completion_rate(tasks)


if __name__ == "__main__":
    unittest.main()
