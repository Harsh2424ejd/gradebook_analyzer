#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Author:  Harsh Vardhan Pratap Singh
# Date:    01-11-2025
# Title:   Gradebook Analyzer
#
# Description: This script allows a user to input student marks either
#              manually or via a CSV file. It then performs statistical
#              analysis, assigns grades, and prints a full report.
# -----------------------------------------------------------------------------

import csv
import statistics
import sys

def print_welcome_menu():
    """Prints the main welcome message and user menu."""
    print("\n" + "="*40)
    print("      Welcome to the Gradebook Analyzer")
    print("="*40)
    print("Please choose an option:")
    print("  1: Manually enter student data")
    print("  2: Load data from a CSV file")
    print("  3: Exit program")
    return input("Enter your choice (1, 2, or 3): ")

def get_manual_input():
    """
    (Task 2a)
    Prompts the user to manually enter student names and marks.
    Returns a dictionary of {name: mark}.
    """
    print("\n--- Manual Data Entry ---")
    print("Enter student name and mark. Press Enter on an empty name to finish.")
    marks_dict = {}
    while True:
        name = input("Enter student name: ").strip()
        if not name:
            break
        
        try:
            mark = int(input(f"Enter mark for {name}: ").strip())
            if 0 <= mark <= 100:
                marks_dict[name] = mark
            else:
                print("Invalid mark. Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numerical mark.")
            
    return marks_dict

def load_from_csv():
    """
    (Task 2b)
    Prompts the user for a CSV filename and loads the data.
    Assumes CSV format: 'Name,Marks' (with a header row)
    Returns a dictionary of {name: mark}.
    """
    print("\n--- Load from CSV File ---")
    filename = input("Enter the CSV filename (e.g., 'grades.csv'): ").strip()
    marks_dict = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row
            print(f"Loading data from '{filename}' (Header: {', '.join(header)})")
            
            for row in reader:
                if not row:  # Skip empty rows
                    continue
                try:
                    name = row[0].strip()
                    mark = int(row[1].strip())
                    marks_dict[name] = mark
                except (ValueError, IndexError):
                    print(f"Skipping invalid row: {row}")
            
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return marks_dict

# --- Task 3: Statistical Analysis Functions ---

def calculate_average(marks_dict):
    """Calculates the average (mean) of all marks."""
    if not marks_dict:
        return 0
    scores = marks_dict.values()
    return sum(scores) / len(scores)

def calculate_median(marks_dict):
    """Calculates the median of all marks."""
    if not marks_dict:
        return 0
    return statistics.median(marks_dict.values())

def get_max_score(marks_dict):
    """Finds the student with the highest score. Returns (name, score)."""
    if not marks_dict:
        return ("N/A", 0)
    # Use max() with a lambda function to find the item with the highest value
    return max(marks_dict.items(), key=lambda item: item[1])

def get_min_score(marks_dict):
    """Finds the student with the lowest score. Returns (name, score)."""
    if not marks_dict:
        return ("N/A", 0)
    # Use min() with a lambda function to find the item with the lowest value
    return min(marks_dict.items(), key=lambda item: item[1])

# --- Task 4: Grade Assignment and Distribution ---

def assign_grades(marks_dict):
    """
    Assigns a letter grade to each student based on their mark.
    Returns a new dictionary {name: grade}.
    """
    grades_dict = {}
    for name, mark in marks_dict.items():
        if mark >= 90:
            grades_dict[name] = "A"
        elif mark >= 80:
            grades_dict[name] = "B"
        elif mark >= 70:
            grades_dict[name] = "C"
        elif mark >= 60:
            grades_dict[name] = "D"
        else:
            grades_dict[name] = "F"
    return grades_dict

def calculate_grade_distribution(grades_dict):
    """Counts the total number of students in each grade category."""
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for grade in grades_dict.values():
        if grade in distribution:
            distribution[grade] += 1
    return distribution

# --- Task 5: Pass/Fail Filter ---

def print_pass_fail_summary(marks_dict, pass_threshold=40):
    """
    Uses list comprehensions to find and print lists of
    passing and failing students.
    """
    # Use dictionary comprehensions to create filtered dicts
    passed_students = {name: score for name, score in marks_dict.items() if score >= pass_threshold}
    failed_students = {name: score for name, score in marks_dict.items() if score < pass_threshold}

    print("\n--- Pass/Fail Summary ---")
    print(f"Pass Mark: {pass_threshold}")
    print(f"\nTotal Students Passed: {len(passed_students)}")
    if passed_students:
        # .keys() returns a view object, list() converts it
        print(f"  Names: {', '.join(passed_students.keys())}") 

    print(f"\nTotal Students Failed: {len(failed_students)}")
    if failed_students:
        print(f"  Names: {', '.join(failed_students.keys())}")

# --- Task 6: Results Table ---

def print_results_table(marks_dict, grades_dict):
    """
    Prints a cleanly formatted table of all students, their marks,
    and their assigned grades.
    """
    print("\n" + "="*40)
    print("         Full Grade Report")
    print("="*40)
    # Define column widths
    print(f"{'Name':<20} {'Marks':<10} {'Grade':<10}")
    print("-" * 40)
    
    # Sort dictionary by name for a consistent report
    for name in sorted(marks_dict.keys()):
        marks = marks_dict[name]
        grade = grades_dict.get(name, 'N/A')
        print(f"{name:<20} {marks:<10} {grade:<10}")
    print("-" * 40)

# --- Bonus: Save to CSV ---

def save_results_to_csv(marks_dict, grades_dict):
    """Saves the final report (Name, Marks, Grade) to a new CSV file."""
    filename = input("\nEnter filename to save results (e.g., 'report.csv'): ").strip()
    if not filename.endswith('.csv'):
        filename += '.csv'
        
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Name', 'Marks', 'Grade'])
            
            # Write data rows
            for name in sorted(marks_dict.keys()):
                writer.writerow([name, marks_dict[name], grades_dict[name]])
        
        print(f"Successfully saved report to '{filename}'")
        
    except IOError:
        print(f"Error: Could not write to file '{filename}'.")
    except Exception as e:
        print(f"An unknown error occurred during save: {e}")

# --- Main Application Loop ---

def main():
    """
    (Task 1 & 6)
    Main function to run the gradebook analyzer.
    Contains the primary application loop.
    """
    while True:
        choice = print_welcome_menu()
        
        marks_data = {}
        
        if choice == '1':
            marks_data = get_manual_input()
        elif choice == '2':
            marks_data = load_from_csv()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            sys.exit()  # Exits the script
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            continue  # Skips the rest of the loop and restarts

        # --- Run Analysis ---
        # Only run analysis if data was successfully loaded
        if marks_data:
            print(f"\n--- Analysis complete for {len(marks_data)} students ---")

            # Task 3: Statistical Analysis
            avg = calculate_average(marks_data)
            median = calculate_median(marks_data)
            (max_name, max_score) = get_max_score(marks_data)
            (min_name, min_score) = get_min_score(marks_data)
            
            print("\n--- Classroom Statistics ---")
            print(f"  Average Score: {avg:.2f}")
            print(f"  Median Score:  {median}")
            print(f"  Highest Score: {max_score} (Student: {max_name})")
            print(f"  Lowest Score:  {min_score} (Student: {min_name})")

            # Task 4: Grade Assignment
            grades_data = assign_grades(marks_data)
            distribution = calculate_grade_distribution(grades_data)
            
            print("\n--- Grade Distribution ---")
            for grade, count in distribution.items():
                print(f"  Grade {grade}: {count} student(s)")
            
            # Task 5: Pass/Fail
            print_pass_fail_summary(marks_data, pass_threshold=40)
            
            # Task 6: Results Table
            print_results_table(marks_data, grades_data)
            
            # Bonus: Save to CSV
            save_choice = input("\nDo you want to save this report to a CSV file? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_results_to_csv(marks_data, grades_data)

        else:
            print("No data loaded. Returning to main menu.")


# Standard Python entry point
if __name__ == "__main__":
    main()