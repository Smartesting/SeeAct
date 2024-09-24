import re
from datetime import datetime


def process_log(log_content):
    sections_to_keep = [
        "Previous Action Analysis",
        "Test Case Progress",
        "Current Webpage Identification",
        "Screenshot Details Analysis",
        "Test Step Assertion Control",
        "Final Answer",
        "Grounding Output",
    ]

    sections_to_not_keep = ["Next Action Based on Webpage and Analysis", "Browser Operation"]

    start_time = None
    output_lines = []
    action_i = 1
    in_section = False

    first_timestamp = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})", log_content)
    if first_timestamp:
        first_time = datetime.strptime(first_timestamp.group(1), "%Y-%m-%d %H:%M:%S,%f")
    else:
        first_time = None

    with open(output_file, "w") as f:
        f.write("\n".join(output_lines))

        for line in log_content.split("\n"):
            timestamp_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (.*)", line)

            if timestamp_match:

                text = timestamp_match.group(2)

                new_action = re.search(f"Action Generation Output", timestamp_match.group(2), re.DOTALL)

                if new_action:
                    output_lines.append(f"\n#########################################################")
                    output_lines.append(f"############### Beginning Action Number {action_i} ###############")
                    output_lines.append(f"######################################################### \n")
                    action_i += 1

                current_time = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S,%f")

                if first_time:
                    time_diff = current_time - first_time
                    minutes, seconds = divmod(time_diff.seconds, 60)
                    relative_time = f"{minutes:02d}mn{seconds:02d}s"

                for section in sections_to_keep:
                    section_text = re.search(f"{section}.*?(?=\n\n|\Z)", text, re.DOTALL)
                    if section_text:
                        current_section = section
                        in_section = True
                        output_lines.append(f"\n{relative_time} - {section}\n")
                        break

                for section in sections_to_not_keep:
                    section_text = re.search(f"{section}.*?(?=\n\n|\Z)", text, re.DOTALL)
                    if section_text:
                        current_section = section
                        in_section = False
                        break

                if in_section:
                    output_lines.append(f"{relative_time} - {text}")

            # if in_section:
            #     if line.strip() and not any(section in line for section in sections_to_keep):
            #         output_lines.append(f"{relative_time} - {text}")
            #     elif any(section in line for section in sections_to_keep) and section != current_section:
            #         in_section = False

    return "\n".join(output_lines)


# Usage
input_file = "benchmark_testing_results/classifieds/classifieds_tc2/classifieds_tc2.log"
output_file = "output_log.txt"

with open(input_file, "r") as file:
    log_content = file.read()

processed_log = process_log(log_content)

# Write the processed log to a new file
with open(output_file, "w") as file:
    file.write(processed_log)

# process_log(input_file, output_file)
