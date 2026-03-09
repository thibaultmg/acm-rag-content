import json

import pytest

from scripts.extract_ids import extract_ids_from_xml


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.mark.parametrize(
    "xml_content, expected_output",
    [
        # Standard case with namespaces
        (
            """<?xml version="1.0" encoding="UTF-8"?>
            <book xmlns="http://docbook.org/ns/docbook" xml:id="book_id">
                <title>Book Title</title>
                <section xml:id="sec_1">
                    <title>Section 1 Title</title>
                </section>
                <section xml:id="sec_2">
                    <title>Section 2 Title</title>
                </section>
            </book>""",
            {
                "Book Title": ["book_id"],
                "Section 1 Title": ["sec_1"],
                "Section 2 Title": ["sec_2"],
            },
        ),
        # Missing namespaces and 'id' instead of 'xml:id'
        (
            """<?xml version="1.0" encoding="UTF-8"?>
            <book id="book_id_no_ns">
                <title>Book No NS</title>
                <section id="sec_1_no_ns">
                    <title>Section 1 No NS</title>
                </section>
            </book>""",
            {"Book No NS": ["book_id_no_ns"], "Section 1 No NS": ["sec_1_no_ns"]},
        ),
        # Duplicate titles mapped to lists of IDs
        (
            """<?xml version="1.0" encoding="UTF-8"?>
            <book id="book_1">
                <title>Duplicate Title</title>
                <section id="sec_1">
                    <title>Duplicate Title</title>
                </section>
                <section id="sec_2">
                    <title>Duplicate Title</title>
                </section>
            </book>""",
            {"Duplicate Title": ["sec_1", "sec_2", "book_1"]},
        ),
        # Deeply nested tags
        (
            """<?xml version="1.0" encoding="UTF-8"?>
            <book id="root">
                <title>Root</title>
                <part id="part_1">
                    <title>Part 1</title>
                    <chapter id="chap_1">
                        <title>Chapter 1</title>
                        <section id="sec_deep">
                            <title>Deep Section</title>
                        </section>
                    </chapter>
                </part>
            </book>""",
            {
                "Root": ["root"],
                "Part 1": ["part_1"],
                "Chapter 1": ["chap_1"],
                "Deep Section": ["sec_deep"],
            },
        ),
        # Missing title entirely
        (
            """<?xml version="1.0" encoding="UTF-8"?>
            <book id="root">
                <section id="no_title_sec">
                </section>
            </book>""",
            {},
        ),
        # Empty title tag
        (
            """<?xml version="1.0" encoding="UTF-8"?>
            <book id="root">
                <title></title>
            </book>""",
            {},
        ),
    ],
)
def test_extract_ids_from_xml(temp_dir, xml_content, expected_output):
    xml_file = temp_dir / "test.xml"
    json_file = temp_dir / "output.json"

    xml_file.write_text(xml_content)

    extract_ids_from_xml(str(xml_file), str(json_file))

    assert json_file.exists()

    with open(json_file) as f:
        data = json.load(f)

    assert data == expected_output
