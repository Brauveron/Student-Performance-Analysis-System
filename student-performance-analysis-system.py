import csv
import os
from abc import ABC, abstractmethod

# ==========================================
# Task 1: Design the Dataset
# ==========================================
def create_dataset(filename="students_dataset.csv"):
    """Creates a CSV dataset with the provided sample records."""
    headers = ["StudentID", "FName", "LName", "Programme", "Math", "English", "Science", "Type"]
    data = [
        ["25/222", "Sandra", "Mutegi", "MDS", 75, 80, 70, "Standard"],
        ["25/224", "Carlos", "Ndunda", "MDS", 90, 85, 88, "Scholarship"],
        ["25/226", "Paul", "Omboga", "MDA", 60, 65, 58, "Standard"],
        ["25/228", "Ruth", "Mwimali", "MDA", 95, 92, 90, "Scholarship"],
        ["25/230", "John", "Doe", "MDS", 40, 50, 45, "Standard"] # Additional record
    ]
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# ==========================================
# Task 2: Student Class, Encapsulation & Abstraction
# Task 6: Method Overloading & Flexible Interfaces
# ==========================================
class Student(ABC):
    """Abstract base class demonstrating encapsulation and abstraction."""
    
    def __init__(self, student_id, fname, lname, programme, math, english, science):
        # Encapsulation: Making attributes private
        self.__student_id = student_id
        self.__fname = fname
        self.__lname = lname
        self.__programme = programme
        self.__marks = {'Math': math, 'English': english, 'Science': science}

    # Access conventions (Getters) to protect data
    @property
    def student_id(self): return self.__student_id
    @property
    def full_name(self): return f"{self.__fname} {self.__lname}"
    @property
    def programme(self): return self.__programme
    @property
    def marks(self): return self.__marks

    # Task 6: Method Overloading (Flexible Interfaces)
    # Python uses *args or default arguments instead of traditional overloading.
    def calculate_average(self, *custom_marks):
        """
        Flexible method: Calculates average from either stored marks (0 args) 
        or a variable number of custom marks passed as arguments.
        """
        if len(custom_marks) == 0:
            scores = list(self.__marks.values())
        else:
            scores = custom_marks
            
        # Validation
        if not all(isinstance(m, (int, float)) for m in scores):
            raise ValueError("All marks must be numerical numbers.")
            
        return sum(scores) / len(scores) if scores else 0

    def determine_grade(self):
        avg = self.calculate_average()
        if avg >= 85: return 'A'
        elif avg >= 70: return 'B'
        elif avg >= 60: return 'C'
        elif avg >= 50: return 'D'
        return 'F'

    # Abstraction: Forcing subclasses to implement this method
    @abstractmethod
    def display_details(self):
        pass

class AIUStudent(Student):
    """Concrete subclass inheriting from Student."""
    
    def display_details(self):
        # Implementation of the abstract method
        return f"Standard Student: {self.full_name} ({self.student_id}) - {self.programme}"

# ==========================================
# Task 4: Inheritance and Method Overriding
# ==========================================
class ScholarshipStudent(AIUStudent):
    """Subclass demonstrating inheritance and method overriding."""
    
    def __init__(self, student_id, fname, lname, programme, math, english, science, scholarship_amount=50000):
        # Using super() to call parent constructor
        super().__init__(student_id, fname, lname, programme, math, english, science)
        self.scholarship_amount = scholarship_amount

    def is_eligible(self):
        # Eligibility logic based on average
        return self.calculate_average() >= 85

    def display_details(self):
        # Method Overriding: Changing inherited behavior
        base_info = super().display_details().replace("Standard Student:", "Scholarship Applicant:")
        status = "Eligible" if self.is_eligible() else "Not Eligible"
        return f"{base_info} | Scholarship Status: {status} (Ksh {self.scholarship_amount})"

# ==========================================
# Task 3: Performance Analyzer & Composition
# Task 7: Report Generation
# ==========================================
class PerformanceAnalyzer:
    """Uses composition to manage a collection of Student objects."""
    
    def __init__(self, students):
        self.students = students

    def highest_average(self):
        return max(self.students, key=lambda s: s.calculate_average())

    def lowest_average(self):
        return min(self.students, key=lambda s: s.calculate_average())

    def class_average(self):
        if not self.students: return 0
        total = sum(s.calculate_average() for s in self.students)
        return total / len(self.students)

    def generate_report(self):
        print("="*75)
        print(f"{'AIU STUDENT PERFORMANCE REPORT':^75}")
        print("="*75)
        
        # Task 5: Polymorphism in action
        # Looping through a mixed collection of AIUStudent and ScholarshipStudent objects.
        # Calling the shared 'display_details()' method executes the appropriate class's version.
        for student in self.students:
            avg = student.calculate_average()
            grade = student.determine_grade()
            
            # Polymorphic method call
            print(student.display_details()) 
            print(f"Marks: {student.marks} | Avg: {avg:.2f} | Grade: {grade}")
            print("-" * 75)

        # Summary
        highest = self.highest_average()
        lowest = self.lowest_average()
        
        print(f"{'CLASS SUMMARY':^75}")
        print("="*75)
        print(f"Total Students   : {len(self.students)}")
        print(f"Overall Average  : {self.class_average():.2f}")
        print(f"Highest Average  : {highest.full_name} ({highest.calculate_average():.2f})")
        print(f"Lowest Average   : {lowest.full_name} ({lowest.calculate_average():.2f})")
        print("="*75)

# ==========================================
# Main Execution
# ==========================================
def main():
    filename = "students_dataset.csv"
    create_dataset(filename)
    
    students_list = []
    
    # Load dataset and populate objects
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Type'] == 'Standard':
                student = AIUStudent(
                    row['StudentID'], row['FName'], row['LName'], row['Programme'], 
                    float(row['Math']), float(row['English']), float(row['Science'])
                )
            else:
                student = ScholarshipStudent(
                    row['StudentID'], row['FName'], row['LName'], row['Programme'], 
                    float(row['Math']), float(row['English']), float(row['Science'])
                )
            students_list.append(student)
            
    # Task 6 Demonstration Check:
    # Calculating an average bypassing the stored marks via flexible arguments
    print(f"\n[Test] Overloaded Average for 3 random marks (99, 98, 97): {students_list[0].calculate_average(99, 98, 97):.2f}\n")

    # Analyze and Report
    analyzer = PerformanceAnalyzer(students_list)
    analyzer.generate_report()

    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    main()