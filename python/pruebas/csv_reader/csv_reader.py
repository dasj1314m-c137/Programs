import csv
import sys

def get_data(file):
    with open(file, 'r') as file:
        data = list(csv.DictReader(file))
        return data, data[0].keys()

def extract_data(data, wanted_sections):
    extracted_data = []
    for row in data:
        row = {section: row[section] for section in wanted_sections}
        extracted_data.append(row)
    return extracted_data, ' - '.join(formatted_wanted_sections)

def check_sections(all_sections, wanted_sections):
    not_found_sections = [section for section in wanted_sections if section not in all_sections]
    return not_found_sections

def format_wanted_sections(wanted_sections):
    if "," in wanted_sections:
        return [section.strip() for section in wanted_sections.split(",")]
    else:
        return [wanted_sections.strip()]

def join_sections(sections):
    if len(sections) == 1:
        return sections[0]
    else:
        return '\n'.join([f"  - {section}" for section in sections])

def join_data(data):
    return "\n".join([f"  - {' - '.join(row.values())}" for row in data])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 csv_reader.py <filename>")
        sys.exit(1)
    file = sys.argv[1]

    data, all_sections = get_data(file)

    while True:
        print("Available sections:")
        print(join_sections(all_sections))
        wanted_sections = input("Enter the section or sections you want to extract (comma-separated): ")

        if not wanted_sections:
            print("No sections entered, please try again.")
            continue

        formatted_wanted_sections = format_wanted_sections(wanted_sections)

        not_found_sections = check_sections(all_sections, formatted_wanted_sections)
        if not_found_sections:
            print(f"Sections not found:\n{join_sections(not_found_sections)}.\nPlease try again.")
            continue
        break

    extracted_data, extracted_sections = extract_data(data, formatted_wanted_sections)
    print(f"Extracted Data: {extracted_sections}")
    print(join_data(extracted_data))