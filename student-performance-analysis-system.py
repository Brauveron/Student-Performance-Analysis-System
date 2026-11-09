import csv
import os
from abc import ABC, abstractmethod

# ---------------------------------------------------------
# 1. Abstraction & Encapsulation
# ---------------------------------------------------------
class Student(ABC):
    """Abstract base class representing a generic student."""
    
    def __init__(self, student_id, name, scores):
        # Encapsulation: Making attributes private
        self.__student_id = student_id
        self.__name = name
        self.__scores = scores

    # Getters to access private attributes safely
    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @property
    def scores(self):
        return self.__scores

    def get_average(self):
        """Calculates the average score."""
        if not self.__scores:
            return 0
        return sum(self.__scores) / len(self.__scores)

    # Method Overloading Simulation: Python doesn't support traditional method overloading.
    # We simulate it using variable-length arguments (*args) and default parameters.
    def apply_bonus(self, *bonus_points, flat_bonus=0):
        """
        Applies bonus points flexibly. 
        Can accept multiple specific bonus points or a single flat bonus.
        """
        if bonus_points:
            total_bonus = sum(bonus_points)
            self.__scores = [score + total_bonus for score in self.__scores]
        else:
            self.__scores = [score + flat_bonus for score in self.__scores]

    # Abstract methods enforcing polymorphism in child classes
    @abstractmethod
    def calculate_grade(self):
        pass

    @abstractmethod
    def check_scholarship_eligibility(self):
        pass


# ---------------------------------------------------------
# 2. Inheritance, Polymorphism & Method Overriding
# ---------------------------------------------------------
class UndergradStudent(Student):
    """Derived class for Undergraduate Students."""
    
    def calculate_grade(self):
        avg = self.get_average()
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        return 'F'

    def check_scholarship_eligibility(self):
        # Undergrads need an 85 or higher for a scholarship
        return self.get_average() >= 85


class GradStudent(Student):
    """Derived class for Graduate Students."""
    
    def calculate_grade(self):
        # Graduate students have stricter grading curves
        avg = self.get_average()
        if avg >= 92: return 'A'
        elif avg >= 85: return 'B'
        elif avg >= 75: return 'C'
        return 'F' 

    def check_scholarship_eligibility(self):
        # Grads need a 90 or higher for a scholarship
        return self.get_average() >= 90


# ---------------------------------------------------------
# 3. Performance Analyzer
# ---------------------------------------------------------
class PerformanceAnalyzer:
    """Class to analyze a cohort of students."""
    
    def __init__(self, students):
        self.students = students

    def get_class_average(self):
        if not self.students:
            return 0
        total_sum = sum(student.get_average() for student in self.students)
        return total_sum / len(self.students)

    def get_highest_performer(self):
        if not self.students: return None
        # Finds the student with the maximum average
        return max(self.students, key=lambda s: s.get_average())

    def get_lowest_performer(self):
        if not self.students: return None
        # Finds the student with the minimum average
        return min(self.students, key=lambda s: s.get_average())


# ---------------------------------------------------------
# 4. Main Execution & Report Generation
# ---------------------------------------------------------
def create_sample_csv(filename="students.csv"):
    """Helper method to create a sample dataset."""
    headers = ['ID', 'Name', 'Math', 'Science', 'English', 'Type']
    data = [
        ['101', 'Alice Johnson', '88', '92', '85', 'Undergrad'],
        ['102', 'Bob Smith', '65', '70', '68', 'Undergrad'],
        ['103', 'Charlie Davis', '95', '96', '93', 'Grad'],
        ['104', 'Diana Prince', '78', '82', '80', 'Grad']
    ]
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    csv_file = "students.csv"
    create_sample_csv(csv_file)

    students_list = []

    # Read the CSV and instantiate polymorphic objects
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_id = row['ID']
            name = row['Name']
            scores = [int(row['Math']), int(row['Science']), int(row['English'])]
            student_type = row['Type']

            if student_type == 'Undergrad':
                student = UndergradStudent(student_id, name, scores)
            else:
                student = GradStudent(student_id, name, scores)
            
            # Demonstrating the overloaded/flexible method: 
            # Alice gets multiple specific bonuses (*args), Bob gets a flat default bonus
            if name == 'Alice Johnson':
                student.apply_bonus(2, 3) # Adds 5 points to all scores
            elif name == 'Bob Smith':
                student.apply_bonus(flat_bonus=5) # Adds 5 points using default kwarg
                
            students_list.append(student)

    # Analyze Data
    analyzer = PerformanceAnalyzer(students_list)
    
    # Generate Report
    print("="*60)
    print(f"{'STUDENT PERFORMANCE REPORT':^60}")
    print("="*60)
    
    for s in students_list:
        avg = s.get_average()
        grade = s.calculate_grade()
        scholarship = "Eligible" if s.check_scholarship_eligibility() else "Not Eligible"
        
        print(f"ID: {s.student_id} | Name: {s.name:<15} | Type: {s.__class__.__name__}")
        print(f"Scores: {s.scores} | Average: {avg:.2f}")
        print(f"Grade: {grade} | Scholarship: {scholarship}")
        print("-" * 60)

    # Class Summary
    highest = analyzer.get_highest_performer()
    lowest = analyzer.get_lowest_performer()
    
    print(f"{'CLASS SUMMARY':^60}")
    print("="*60)
    print(f"Total Students Evaluated : {len(students_list)}")
    print(f"Overall Class Average    : {analyzer.get_class_average():.2f}")
    print(f"Highest Performer        : {highest.name} ({highest.get_average():.2f})")
    print(f"Lowest Performer         : {lowest.name} ({lowest.get_average():.2f})")
    print("="*60)

    # Cleanup the generated CSV (optional)
    if os.path.exists(csv_file):
        os.remove(csv_file)

if __name__ == "__main__":
    main()