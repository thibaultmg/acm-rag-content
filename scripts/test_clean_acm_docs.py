import xml.etree.ElementTree as ET

import pytest

from scripts.clean_acm_docs import NS, clean_docbook, is_navigation_list


def create_itemizedlist(xml_string):
    ET.register_namespace("db", NS["db"])
    xml_with_ns = f'<db:itemizedlist xmlns:db="{NS["db"]}">{xml_string}</db:itemizedlist>'
    return ET.fromstring(xml_with_ns)


@pytest.mark.parametrize(
    "xml_content, expected",
    [
        (
            """
        <db:listitem>
            <db:para>
                <db:link linkend="id1">Only link text</db:link>
            </db:para>
        </db:listitem>
        """,
            True,
        ),
        (
            """
        <db:listitem>
            <db:para>
                This is some regular text that happens to have a <db:link linkend="id1">link</db:link> in it.
            </db:para>
        </db:listitem>
        """,
            False,
        ),
        (
            """
        <db:listitem>
            <db:para>
                Just text, no links at all.
            </db:para>
        </db:listitem>
        """,
            False,
        ),
        ("", False),
    ],
)
def test_is_navigation_list(xml_content, expected):
    ulist = create_itemizedlist(xml_content)
    assert is_navigation_list(ulist) == expected


def test_removes_navigation_lists(tmp_path):
    input_xml = """<?xml version='1.0' encoding='utf-8'?>
<article xmlns="http://docbook.org/ns/docbook" version="5.0" xml:lang="en">
    <para>See also:</para>
    <itemizedlist>
        <listitem><para><xref linkend="id1"/></para></listitem>
    </itemizedlist>
</article>
"""
    test_file = tmp_path / "test_nav.xml"
    test_file.write_text(input_xml, encoding="utf-8")
    clean_docbook(str(test_file))
    root = ET.parse(str(test_file)).getroot()
    assert len(root.findall(".//db:itemizedlist", NS)) == 0
    paras = ["".join(p.itertext()).strip() for p in root.findall(".//db:para", NS)]
    assert "See also:" not in paras


def test_converts_tables_to_lists(tmp_path):
    input_xml = """<?xml version='1.0' encoding='utf-8'?>
<article xmlns="http://docbook.org/ns/docbook" version="5.0" xml:lang="en">
    <table>
        <tgroup cols="2">
            <thead>
                <row><entry>H1</entry><entry>H2</entry></row>
            </thead>
            <tbody>
                <row><entry>V1</entry><entry>V2</entry></row>
            </tbody>
        </tgroup>
    </table>
</article>
"""
    test_file = tmp_path / "test_table.xml"
    test_file.write_text(input_xml, encoding="utf-8")
    clean_docbook(str(test_file))
    root = ET.parse(str(test_file)).getroot()
    assert len(root.findall(".//db:table", NS)) == 0
    list_items = root.findall(".//db:listitem", NS)
    assert len(list_items) == 1
    assert "H1: V1 - H2: V2" in "".join(list_items[0].itertext()).strip()


def test_extracts_list_titles(tmp_path):
    input_xml = """<?xml version='1.0' encoding='utf-8'?>
<article xmlns="http://docbook.org/ns/docbook" version="5.0" xml:lang="en">
    <itemizedlist>
        <title>Prerequisites</title>
        <listitem><simpara>Requirement</simpara></listitem>
    </itemizedlist>
</article>
"""
    test_file = tmp_path / "test_title.xml"
    test_file.write_text(input_xml, encoding="utf-8")
    clean_docbook(str(test_file))
    root = ET.parse(str(test_file)).getroot()
    assert len(root.findall(".//db:itemizedlist/db:title", NS)) == 0
    strong = root.find('.//db:emphasis[@role="strong"]', NS)
    assert strong is not None
    assert strong.text == "Prerequisites"


def test_removes_additional_resources(tmp_path):
    input_xml = """<?xml version='1.0' encoding='utf-8'?>
<article xmlns="http://docbook.org/ns/docbook" version="5.0" xml:lang="en">
    <section>
        <title>Additional resources</title>
        <para>Content to remove</para>
    </section>
</article>
"""
    test_file = tmp_path / "test_resources.xml"
    test_file.write_text(input_xml, encoding="utf-8")
    clean_docbook(str(test_file))
    root = ET.parse(str(test_file)).getroot()
    section_titles = ["".join(t.itertext()).strip().lower() for t in root.findall(".//db:title", NS)]
    assert "additional resources" not in section_titles
    paras = ["".join(p.itertext()).strip() for p in root.findall(".//db:para", NS)]
    assert "Content to remove" not in paras


def test_removes_images(tmp_path):
    input_xml = """<?xml version='1.0' encoding='utf-8'?>
<article xmlns="http://docbook.org/ns/docbook" version="5.0" xml:lang="en">
    <para>Following image:</para>
    <figure>
        <mediaobject>
            <imageobject><imagedata fileref="img.png"/></imageobject>
        </mediaobject>
    </figure>
</article>
"""
    test_file = tmp_path / "test_image.xml"
    test_file.write_text(input_xml, encoding="utf-8")
    clean_docbook(str(test_file))
    root = ET.parse(str(test_file)).getroot()
    assert len(root.findall(".//db:figure", NS)) == 0
    paras = ["".join(p.itertext()).strip() for p in root.findall(".//db:para", NS)]
    assert "Following image:" not in paras
