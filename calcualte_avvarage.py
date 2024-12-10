import PyPDF2
import numpy as np

# Function to parse grades from the PDF
def parse_pdf(file_path):
    grades = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                # Example format: "1 121522995 76"
                parts = line.split()
                if len(parts) >= 3:  # Each line should have at least 3 parts
                    try:
                        score = int(parts[-1])  # The last part should be the grade
                        grades.append(score)
                    except ValueError:
                        continue  # Skip lines with non-numeric grades like "Absent"
    return grades

# Assign letter grades using bell curve
def assign_grades_bell_curve(grades):
    mean = np.mean(grades)  # Class mean
    std_dev = np.std(grades)  # Standard deviation

    letter_grades = {}
    for i, grade in enumerate(grades):
        if grade >= mean + 1.5 * std_dev:
            letter = "AA"
        elif grade >= mean + 0.5 * std_dev:
            letter = "BA"
        elif grade >= mean - 0.5 * std_dev:
            letter = "BB"
        elif grade >= mean - 1.5 * std_dev:
            letter = "CC"
        elif grade >= mean - 2 * std_dev:
            letter = "DD"
        else:
            letter = "FF"
        letter_grades[i + 1] = letter

    return letter_grades, mean, std_dev

# Main function to calculate and display grades
def main(file_path):
    grades = parse_pdf(file_path)
    if not grades:
        print("No grades found.")
        return

    valid_grades = [g for g in grades if isinstance(g, int)]  # Filter valid numeric grades
    if valid_grades:
        letter_grades, class_mean, std_dev = assign_grades_bell_curve(valid_grades)

        print(f"Class Mean: {class_mean:.2f}")
        print(f"Standard Deviation: {std_dev:.2f}")
        print("Letter Grades:")
        for student, letter in letter_grades.items():
            print(f"Student {student}: {letter}")
    else:
        print("No valid grades found.")

# Usage
pdf_file_path = "yourfile_path.pdf"  # Provide the path to your PDF file
main(pdf_file_path)
