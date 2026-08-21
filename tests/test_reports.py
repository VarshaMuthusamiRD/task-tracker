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


if __name__ == "__main__":
    unittest.main()
