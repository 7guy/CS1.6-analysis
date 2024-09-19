import argparse
import json
from datetime import datetime
import re
import os


def parse_log_entry(log_entry, distance_context,headshot_context):
    pattern = re.compile(r'^L (\d+/\d+/\d+ - \d+:\d+:\d+): (.+)$')

    match = pattern.match(log_entry)
    if match:
        timestamp_str, log_info = match.groups()
        timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y - %H:%M:%S")

        # Extract relevant information based on log_info
        event = {"timestamp": timestamp}

        if "World triggered" in log_info:
            event["event_type"] = log_info.split('"')[1]
        elif "killed" in log_info:
            match = re.match(r'^"(.+)<(\d+)><(.+)><(.+)>" killed "(.+)<(\d+)><(.+)><(.+)>" with "(.+)"$', log_info)
            if match:
                killer_name, _, killer_id, _, victim_name, _, victim_id, _, weapon = match.groups()
                event.update({
                    "event_type": "Player_Kill",
                    "killer_name": killer_name,
                    "killer_id": killer_id,
                    "victim_name": victim_name,
                    "victim_id": victim_id,
                    "weapon": weapon,
                })

                # Check if distance information is present in the log entry
                if distance_context:
                    event["distance"] = distance_context["distance"]
                    distance_context.clear()

                # Check if the kill was a headshot
                if headshot_context.get("headshot", False):
                    event["headshot"] = True
                else:
                    event["headshot"] = False

                # Clear the headshot context after processing the kill event
                headshot_context.clear()

        elif "triggered" in log_info:
            trigger_match = re.match(r'^"(.+)<(\d+)><(.+)><(.+)>" triggered "(.+)"$', log_info)
            if trigger_match:
                trigger_name, _, _, _, trigger_event = trigger_match.groups()
                event["event_type"] = trigger_event
                event["triggered_by"] = {"name": trigger_name}

        # Check if distance information is present in the log entry, before 'player_kill' log
        distance_match = re.search(r'from a distance of (\d+) meters', log_info)
        if distance_match:
            distance_context["distance"] = int(distance_match.group(1))

        # Check if the current log entry indicates a headshot
        if "killed" in log_info and "headshot" in log_info:
            headshot_context["headshot"] = True

        return event

    return None


def parse_log_file(log_file_path):
    parsed_data = []
    distance_context = {}
    headshot_context = {}

    with open(log_file_path, "r") as file:
        for log_entry in file:
            parsed_entry = parse_log_entry(log_entry, distance_context, headshot_context)
            if parsed_entry:
                parsed_data.append(parsed_entry)

    return parsed_data


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument("-v","--verbose", action="store_true", help="print details of copied log files.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    log_files_folder = os.path.expanduser("~/PycharmProjects/cs_analytics/logs/log_files")
    output_folder = os.path.expanduser("~/PycharmProjects/cs_analytics/database/parsed_data")
    num_of_parsed_files = 0

    for file_name in os.listdir(log_files_folder):
        log_file_path = os.path.join(log_files_folder, file_name)

        # Check if the item in the folder is a file (not a subdirectory)
        if os.path.isfile(log_file_path):
            parsed_data = parse_log_file(log_file_path)

            # Output parsed data to a JSON file
            output_path = os.path.join(output_folder ,f"{file_name.replace('.log', '_parsed.json')}")
            with open(output_path, "w") as output_file:
                json.dump(parsed_data, output_file, default=str, indent=2)

            num_of_parsed_files +=1

            if args.verbose:
                print(f"Successfully parsed '{file_name}' and saved the parsed data to '{output_path}'.")

    print(f"Successfully parsed '{num_of_parsed_files}' files and saved the parsed data to '{output_folder}'.")


if __name__ == "__main__":
    main()
