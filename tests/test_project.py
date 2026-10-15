"""Testes de integridade do material que rodam sem GPU."""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    with (ROOT / "data" / f"{name}.jsonl").open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def normalize(s):
    import unicodedata
    return "".join(
        char for char in unicodedata.normalize("NFKD", s.lower())
        if not unicodedata.combining(char)
    )


class DataIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.splits = {s: load(s) for s in ("train", "val", "test")}

    def test_expected_counts(self):
        self.assertEqual({s: len(rows) for s, rows in self.splits.items()},
                         {"train": 96, "val": 16, "test": 16})

    def test_no_duplicate_ids_or_prompts_across_splits(self):
        rows = sum(self.splits.values(), [])
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(len(rows), len({r["prompt"] for r in rows}))

    def test_required_fields_and_reference_keywords(self):
        for split, rows in self.splits.items():
            for row in rows:
                with self.subTest(split=split, id=row["id"]):
                    for name in ("id", "category", "prompt", "answer",
                                 "expected_keywords"):
                        self.assertIn(name, row)
                    self.assertIn("Causa:", row["answer"])
                    self.assertIn("Correção:", row["answer"])
                    self.assertIn("Código corrigido:", row["answer"])
                    self.assertIn("Erro observado:", row["prompt"])
                    self.assertTrue(row["expected_keywords"])
                    for term in row["expected_keywords"]:
                        self.assertIn(normalize(term), normalize(row["answer"]))

    def test_all_categories_present_in_each_split(self):
        categories = {
            s: {item["category"] for item in rows}
            for s, rows in self.splits.items()
        }
        self.assertEqual(categories["train"], categories["val"])
        self.assertEqual(categories["train"], categories["test"])
        self.assertGreaterEqual(len(categories["train"]), 12)


if __name__ == "__main__":
    unittest.main()
