import os

class Semester:
    """Contains classes and their grades"""

    def __init__(self, name: str, manager):
        """Sets up a Semester instance"""
        self.name = name
        self.classes = {}
        self.manager = manager

    def add_class(self, class_name: str, earned: int, total: int):
        """Adds a class to semester"""
        self.classes[class_name] = (earned, total)

    def remove_class(self, class_name: str):
        """Removes class from the semester if it's already there"""
        if class_name in self.classes:
            del self.classes[class_name]

    def get_classes(self):
        """Gets classes and their grades for the semester"""
        return self.classes.items()

    def string_convert(self) -> str:
        """Converts semester data to a string"""
        return f"{self.name}\n" + "\n".join(
            [f"{cls}: {earned}/{total}" for cls, (earned, total) in self.classes.items()]
        )

    def calculate_class_grades(self):
        """Finds letter grade for all classes in the semester"""
        grades = {}
        for class_name, (earned, total) in self.classes.items():
            grade = grade_calculator(earned, total)
            grades[class_name] = grade
        return grades

    def update_classes(self, updated_classes_list):
        """Updates classes and saves changes to the file"""
        for class_name, earned, total in updated_classes_list:
            self.add_class(class_name, earned, total)

        self.manager.save_info()

class SemesterManager:
    """Helps with saving, loading, and updating semesters"""
    def __init__(self, file_path: str = "classes.txt"):
        """Starts the SemesterManager instance"""
        self.file_path = file_path
        self.semesters = self.load_data()

    def load_data(self):
        """Loads semester data from file"""
        if not os.path.exists(self.file_path):
            return []

        semesters = []
        with open(self.file_path, "r") as file:
            current_semester = None
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if "Semester" in line:
                    if current_semester:
                        semesters.append(current_semester)
                    current_semester = Semester(line, self)
                elif current_semester:
                    try:
                        class_name, scores = line.split(": ")
                        earned, total = map(int, scores.split("/"))
                        current_semester.add_class(class_name, earned, total)
                    except ValueError:
                        print(f"Skipping line: {line}")
                        continue
            if current_semester:
                semesters.append(current_semester)
        return semesters

    def save_info(self):
        """Saves semester data back to file"""
        with open(self.file_path, "w") as file:
            for semester in self.semesters:
                file.write(semester.string_convert() + "\n\n")

    def add_semester(self, semester: Semester):
        """Adds a new semester and saves the data"""
        self.semesters.append(semester)
        self.save_info()

    def delete_semester(self, semester_name: str):
        """Deletes a semester and saves updated data"""
        self.semesters = [sem for sem in self.semesters if sem.name != semester_name]
        self.save_info()

    def update_semester(self, semester_name: str, updated_semester: Semester):
        """Updates existing semester and saves the changes"""
        for index, semester in enumerate(self.semesters):
            if semester.name == semester_name:
                self.semesters[index] = updated_semester
                break
        self.save_info()

def grade_calculator(earned, total):
    """Calculates letter grade based off earned/total points"""
    score = int(earned)
    best = int(total)
    if score >= best - 10:
        return 'A'
    elif score >= best - 20:
        return 'B'
    elif score >= best - 30:
        return 'C'
    elif score >= best - 40:
        return 'D'
    else:
        return 'F'
