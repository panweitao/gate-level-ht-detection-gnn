import tempfile
import unittest
from pathlib import Path

from tools.validate_prepared_data import discover_pairs, validate_pair


def content_line(node_id: str, label: int) -> str:
    features = " ".join(str(index / 10) for index in range(24))
    return f"{node_id} {features} {label}\n"


class PreparedDataValidationTests(unittest.TestCase):
    def test_valid_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = root / "demo.content"
            cites = root / "demo.cites"
            content.write_text(content_line("0", 0) + content_line("1", 1), encoding="utf-8")
            cites.write_text("0 1\n", encoding="utf-8")

            stats = validate_pair(content, cites)

            self.assertEqual(stats.nodes, 2)
            self.assertEqual(stats.edges, 1)
            self.assertEqual(stats.trojan_nodes, 1)
            self.assertEqual(discover_pairs(root), [(content, cites)])

    def test_rejects_wrong_feature_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = root / "demo.content"
            cites = root / "demo.cites"
            content.write_text("0 1.0 0\n", encoding="utf-8")
            cites.write_text("", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "expected 26 fields"):
                validate_pair(content, cites)

    def test_rejects_unknown_edge_endpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = root / "demo.content"
            cites = root / "demo.cites"
            content.write_text(content_line("0", 0), encoding="utf-8")
            cites.write_text("0 99\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "unknown node"):
                validate_pair(content, cites)


if __name__ == "__main__":
    unittest.main()
