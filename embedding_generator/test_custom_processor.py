import json
import os
import tempfile
import unittest

from custom_processor import (
    AnchorLinkNodeParser,
    CustomMetadataProcessor,
    get_anchor_id,
    slugify,
)
from llama_index.core.schema import Document


class TestCustomProcessor(unittest.TestCase):
    def test_slugify(self):
        cases = [
            ("Hello World", "hello-world"),
            ("Test-Case", "test-case"),
            ("Weird   Spaces", "weird-spaces"),
            ("Special!@#Chars", "specialchars"),
            ("Unicode-🚀", "unicode-"),
            ("-Leading and Trailing-", "-leading-and-trailing-"),
            (None, ""),
            ("", ""),
            (123, ""),  # Type safety
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(slugify(text), expected)

    def test_url_function_main_to_index(self):
        root = os.path.abspath(os.sep)
        cases = [
            (os.path.join(root, "docs", "acm", "main.md"), "http://example.com/index"),
            (
                os.path.join(root, "docs", "acm", "folder", "main.md"),
                "http://example.com/folder/index",
            ),
            (
                os.path.join(root, "docs", "acm", "main_file.md"),
                "http://example.com/main_file",
            ),
            (os.path.join(root, "docs", "acm", "main"), "http://example.com/index"),
            (
                os.path.join(root, "docs", "acm", "domain.md"),
                "http://example.com/domain",
            ),
        ]

        processor = CustomMetadataProcessor(os.path.join(root, "docs", "acm"), "http://example.com/")
        for file_path, expected in cases:
            with self.subTest(file_path=file_path):
                self.assertEqual(processor.url_function(file_path), expected)

    def test_url_function_rename_map(self):
        root = os.path.abspath(os.sep)
        cases = [
            (
                os.path.join(root, "docs", "combined", "acm_2.15", "main.md"),
                "http://example.com/acm/2.15/index",
            ),
            (
                os.path.join(root, "docs", "combined", "thanos_latest", "query.md"),
                "http://example.com/thanos/latest/query",
            ),
            (
                os.path.join(root, "docs", "combined", "unmapped", "file.md"),
                "http://example.com/unmapped/file",
            ),
        ]

        rename_map = {"acm_2.15": "acm/2.15", "thanos_latest": "thanos/latest"}

        processor = CustomMetadataProcessor(os.path.join(root, "docs", "combined"), "http://example.com/", rename_map)
        for file_path, expected in cases:
            with self.subTest(file_path=file_path):
                self.assertEqual(processor.url_function(file_path), expected)

    def test_get_anchor_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock header_map.json
            map_file = os.path.join(tmpdir, "header_map.json")
            with open(map_file, "w") as f:
                json.dump(
                    {
                        "Known Header": "custom-id-123",
                        "List Header": ["custom-id-list-1", "custom-id-list-2"],
                        "Underscore Header": "_custom-id-underscore",
                    },
                    f,
                )

            mock_file = os.path.join(tmpdir, "some_doc.md")

            cases = [
                (mock_file, "Known Header", "custom-id-123"),  # Match from JSON
                (
                    mock_file,
                    "List Header",
                    "custom-id-list-1",
                ),  # Match first element of list
                (
                    mock_file,
                    "Underscore Header",
                    "custom-id-underscore",
                ),  # Leading underscore removed
                (mock_file, "Unknown Header", "unknown-header"),  # Fallback to slugify
                (None, "Valid Header", "valid-header"),  # Type safety for file_path
                ("", "Valid Header", "valid-header"),  # Type safety for file_path
            ]

            for file_path, header_text, expected in cases:
                with self.subTest(file_path=file_path, header_text=header_text):
                    self.assertEqual(get_anchor_id(file_path, header_text), expected)

    def test_anchor_link_node_parser(self):
        parser = AnchorLinkNodeParser()

        # We need mock documents with nodes. The easiest is to parse a simple document and inspect nodes.
        # MarkdownNodeParser will create nodes and overwrite header_path metadata.
        # The node for "## Main Title" will get header_path="/Top Level/"
        doc = Document(
            text="# Top Level\n## Main Title\nSome text here.",
            metadata={
                "docs_url": "http://example.com/page",
                "file_path": "/fake/path/doc.md",
            },
        )

        nodes = parser.get_nodes_from_documents([doc])
        self.assertTrue(len(nodes) > 1)

        # The first node is "# Top Level" with header_path="/"
        # The second node is "## Main Title" with header_path="/Top Level/"
        target_node = nodes[1]

        self.assertIn("docs_url", target_node.metadata)
        # The header leaf is 'Main Title' from the node text, so anchor should be 'main-title'
        self.assertEqual(target_node.metadata["docs_url"], "http://example.com/page#main-title")
        self.assertEqual(target_node.metadata["url"], "http://example.com/page#main-title")

        # Type safety / Missing metadata checks
        doc2 = Document(text="No metadata doc.")
        nodes2 = parser.get_nodes_from_documents([doc2])
        for node in nodes2:
            self.assertNotIn("docs_url", node.metadata)

        # Test safety checks for malformed metadata using mocking to avoid logic duplication
        from unittest.mock import patch

        from llama_index.core.node_parser import MarkdownNodeParser
        from llama_index.core.schema import TextNode

        bad_node = TextNode(text="Bad metadata doc.")
        bad_node.metadata = {
            "header_path": ["List", "Instead", "Of", "String"],
            "docs_url": "http://example.com/page",
            "file_path": "/fake/path/doc.md",
        }

        # Intercept the base class call to return our malformed node
        with patch.object(MarkdownNodeParser, "get_nodes_from_documents", return_value=[bad_node]):
            # This will now call our patched base method, and then run the REAL production loop logic
            nodes3 = parser.get_nodes_from_documents([])
            for node in nodes3:
                # Should not crash, and should skip processing since header_path is not a string
                self.assertEqual(node.metadata["docs_url"], "http://example.com/page")


if __name__ == "__main__":
    unittest.main()
