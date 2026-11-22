import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from csv_profiler import profile_csv
from retry import retry


class CSVProfilerTests(unittest.TestCase):
    def test_counts_and_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("id,name\n1,Ada\n1,\n2,Grace\n", encoding="utf-8")
            output = profile_csv(path, ["id"])
            self.assertEqual(output["rows"], 3)
            self.assertEqual(output["duplicate_keys"], 1)
            self.assertEqual(output["columns"]["name"]["blank_count"], 1)

    def test_empty_csv_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                profile_csv(path)

    def test_unknown_key(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("id\n1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                profile_csv(path, ["other"])

    def test_retry_retries_transient_error(self):
        attempts = []
        def flaky():
            attempts.append(1)
            if len(attempts) == 1:
                raise TimeoutError("temporary")
            return "done"
        self.assertEqual(retry(flaky, attempts=2, base_delay=0), "done")
        self.assertEqual(len(attempts), 2)

    def test_retry_validates_attempts(self):
        with self.assertRaises(ValueError):
            retry(lambda: 1, attempts=0)


if __name__ == "__main__":
    unittest.main()
