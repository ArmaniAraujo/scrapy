# Author: Shahak Rozenblat

# Purpose: Analyze pylint output for easier reporting.
# Please further analyze the output of this script as results vary and may not be accurate.

# Description: 
# Pylint categorizes its message outputs to the following categories: 
# Fatal: Critical issues that may cause the program to crash or terminate abruptly. These should be addressed immediately.
# Error: Serious issues that may lead to bugs, incorrect behavior, or unexpected results. These should be fixed as soon as possible.
# Warning: Suggestions for potential issues or areas of improvement. While not critical, addressing these warnings can enhance code quality.
# Convention: Suggestions related to code style and conventions. Following conventions makes the code more readable and maintainable.
# Refactor: Suggestions for code refactoring to improve the structure, readability, or performance of the code.
# Information: Messages that provide additional information about the analysis process or code.

# IMPORTANT: 
# We will consider “potential bugs” as anything in the Fatal or Error category, and anything else as a false positive.
# This will be the "Estimated False Positive Rate" in the output.
# This is important to analyze and potential talking point as it may not be accurate depending on the reported Errors / Fatals.

# Learn more here: https://pylint.readthedocs.io/en/latest/user_guide/messages/messages_overview.html 

# How to run:
# Run pylint on your project, save output as "pylint_out.txt"
# Then run this script as below: 
# python3 analyze_pylint.py pylint_out.txt analysis_report.txt

import argparse

def parse_pylint_output(output_file):
    analysis = {}
    current_module = None

    with open(output_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("************* Module "):
            current_module = line[len("************* Module "):]
            analysis[current_module] = []
        elif current_module and line:
            try:
                parts = line.split(":")
                file_info = parts[0].strip()
                error_type = parts[3].strip()[0]
                full_error = line
                analysis[current_module].append((file_info, error_type, full_error))
            except Exception:
                continue
    
    return analysis

def generate_statistics(analysis):
    pylint_counts = {'E': 0, 'W': 0, 'C': 0, 'R': 0, 'F': 0, 'I': 0}

    for module_errors in analysis.values():
        for _, error_type, _ in module_errors:
            if error_type in pylint_counts:
                pylint_counts[error_type] += 1

    total_issues = sum(pylint_counts.values())
    left_sum = pylint_counts['F'] + pylint_counts['E'] 

    if left_sum == 0:
        false_positive_rate = 0.0
    else:
        false_positive_rate = 100 - ((left_sum / total_issues) * 100)

    statistics = f"Total Issues: {total_issues}\n"
    statistics += f"Errors: {pylint_counts['E']}\n"
    statistics += f"Warnings: {pylint_counts['W']}\n"
    statistics += f"Conventions: {pylint_counts['C']}\n"
    statistics += f"Refactors: {pylint_counts['R']}\n"
    statistics += f"Fatals: {pylint_counts['F']}\n"
    statistics += f"Informations: {pylint_counts['I']}\n"
    statistics += f"Estimated False Positive Rate: {false_positive_rate:.2f}%\n"

    return statistics

def write_to_file(output_file, analysis, statistics):
    with open(output_file, 'w') as file:
        file.write("Potential Bugs:\n")
        for errors in analysis.values():
            for error in errors:
                if error[1] == 'E':
                    file.write(f"Error: {error[2]}\n")
                if error[1] == 'F':
                    file.write(f"Fatal: {error[2]}\n")

        file.write("\nStatistics:\n")
        file.write(statistics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Pylint output and generate statistics.")
    parser.add_argument("input_file", help="Path to the Pylint output file.")
    parser.add_argument("output_file", help="Path to the output text file.")
    args = parser.parse_args()

    analysis = parse_pylint_output(args.input_file)
    statistics = generate_statistics(analysis)
    write_to_file(args.output_file, analysis, statistics)

    print(f"Analysis completed and saved to '{args.output_file}'.")
