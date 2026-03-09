import argparse
import json
import sys

from lxml import etree as ET


def extract_ids_from_xml(xml_file: str, output_json: str) -> None:
    try:
        id_map: dict[str, list[str]] = {}
        title_map: dict[ET._Element, str] = {}

        context = ET.iterparse(xml_file, events=("start", "end"))
        context = iter(context)
        try:
            _, root = next(context)
        except StopIteration:
            pass
        else:
            for event, elem in context:
                if event == "end":
                    if "title" in elem.tag:
                        parent = elem.getparent()
                        if parent is not None and elem.text:
                            title_map[parent] = elem.text.strip()
                    else:
                        elem_id = elem.get("{http://www.w3.org/XML/1998/namespace}id") or elem.get("id")

                        if elem_id:
                            title_text = title_map.pop(elem, None)

                            if title_text:
                                if title_text not in id_map:
                                    id_map[title_text] = []
                                if elem_id not in id_map[title_text]:
                                    id_map[title_text].append(elem_id)

                    # Complete memory release: clear every element AND remove from parent
                    elem.clear()
                    parent = elem.getparent()
                    if parent is not None:
                        parent.remove(elem)

            root.clear()

        with open(output_json, "w") as f:
            json.dump(id_map, f, indent=2)

        print(f"Extracted {len(id_map)} unique titles to {output_json}")

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error extracting IDs: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract section IDs and titles from DocBook XML.")
    parser.add_argument("xml_file", help="Path to the input DocBook XML file.")
    parser.add_argument("output_json", help="Path to the output JSON file.")

    args = parser.parse_args()

    extract_ids_from_xml(args.xml_file, args.output_json)
