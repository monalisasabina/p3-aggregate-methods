from datetime import datetime
class Student:
    def __init__(self, name):
        self.name = name
        self._enrollments = []

    def enroll(self, course):
        if isinstance(course, Course):
            enrollment = Enrollment(self, course)
            self._enrollments.append(enrollment)
            course.add_enrollment(enrollment)
        else:
            raise TypeError("course must be an instance of Course")

    def get_enrollments(self):
        return self._enrollments.copy()
    
    def course_count(self):
       return len(self._enrollments)

class Course:
    def __init__(self, title):

        self.title = title
        self._enrollments = []

    def add_enrollment(self, enrollment):
        if isinstance(enrollment, Enrollment):
            self._enrollments.append(enrollment)
        else:
            raise TypeError("enrollment must be an instance of Enrollment")

    def get_enrollments(self):
        return self._enrollments.copy()
    
    @classmethod
    def aggregate_enrollments_per_day(cls):
      enrollment_count = {}
      for enrollment in cls.all:
        date = enrollment.get_enrollment_date().date()
        enrollment_count[date] = enrollment_count.get(date, 0) + 1
      return enrollment_count


class Enrollment:
    all = []
    
    def __init__(self, student, course):
        if isinstance(student, Student) and isinstance(course, Course):
            self.student = student
            self.course = course
            self._enrollment_date = datetime.now()
            type(self).all.append(self)
        else:
            raise TypeError("Invalid types for student and/or course")

    def get_enrollment_date(self):
        return self._enrollment_date
    
    def aggregate_average_grade(self):
      # lets assume the grades are stored in a protected attribute called _grades. 
      total_grades = sum(self._grades.values())
      num_courses = len(self._grades)
      average_grade = total_grades / num_courses

      return average_grade
    

    
# Create students
student1 = Student("Alice")
student2 = Student("Bob")

# Create courses
course1 = Course("Math")
course2 = Course("Science")

# Enroll students in courses with grades
student1.enroll(course1)
student1.get_enrollments()[0]._grades = {'Math': 85}  # Assign grades to Alice

student2.enroll(course1)
student2.get_enrollments()[0]._grades = {'Math': 90}  # Assign grades to Bob

student1.enroll(course2)
student1.get_enrollments()[1]._grades = {'Science': 95}  # Assign more grades to Alice

# Output the number of courses each student is enrolled in
print(f"{student1.name} is enrolled in {student1.course_count()} course(s).")
print(f"{student2.name} is enrolled in {student2.course_count()} course(s).")

# Output the average grade for the first enrollment of each student
print(f"{student1.name}'s average grade for {student1.get_enrollments()[0].course.title}: {student1.get_enrollments()[0].aggregate_average_grade()}")
print(f"{student2.name}'s average grade for {student2.get_enrollments()[0].course.title}: {student2.get_enrollments()[0].aggregate_average_grade()}")

# Output the number of enrollments per day
enrollments_per_day = Course.aggregate_enrollments_per_day()
print("\nEnrollments per day:")
for date, count in enrollments_per_day.items():
    print(f"{date}: {count} enrollment(s)")