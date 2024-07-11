import logging
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User
from django.db import transaction
from .models import Assignment, Grade
from notifications.services import NotificationService

logger = logging.getLogger(__name__)

class GradingService:
    
    @staticmethod
    def grade_assignment(assignment_id: int, student_id: int, grade_value: float) -> Grade:
        """
        Grade an assignment for a student.
        """
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            student = User.objects.get(id=student_id)
            
            with transaction.atomic():
                # Check if the assignment is already graded for the student
                existing_grade = Grade.objects.filter(assignment=assignment, student=student).first()
                if existing_grade:
                    logger.warning(f"Assignment {assignment_id} for student {student_id} is already graded.")
                    raise ValidationError("Assignment already graded for this student.")
                
                # Create a new grade instance
                grade = Grade.objects.create(
                    assignment=assignment,
                    student=student,
                    grade=grade_value
                )
                
                # Notify student about the graded assignment
                NotificationService.create_notification(
                    recipient=student,
                    content=f'Your assignment {assignment.title} has been graded with {grade_value}',
                    notification_type_name='grading',
                    content_object=grade
                )
                
                logger.info(f"Graded assignment {assignment_id} for student {student_id} with grade {grade_value}")
                
                return grade
            
        except ObjectDoesNotExist as e:
            logger.error(f"Error grading assignment: {e}")
            raise ValidationError("Assignment or Student not found.")
    
    @staticmethod
    def update_grade(grade_id: int, new_grade_value: float) -> Grade:
        """
        Update an existing grade.
        """
        try:
            grade = Grade.objects.get(id=grade_id)
            
            with transaction.atomic():
                # Update the grade value
                grade.grade = new_grade_value
                grade.save()
                
                # Notify student about the updated grade
                NotificationService.create_notification(
                    recipient=grade.student,
                    content=f'Your grade for assignment {grade.assignment.title} has been updated to {new_grade_value}',
                    notification_type_name='grading',
                    content_object=grade
                )
                
                logger.info(f"Updated grade {grade_id} to {new_grade_value}")
                
                return grade
            
        except ObjectDoesNotExist as e:
            logger.error(f"Error updating grade: {e}")
            raise ValidationError("Grade not found.")
    
    @staticmethod
    def delete_grade(grade_id: int):
        """
        Delete a grade entry.
        """
        try:
            grade = Grade.objects.get(id=grade_id)
            grade.delete()
            logger.info(f"Deleted grade {grade_id}")
            
        except ObjectDoesNotExist as e:
            logger.error(f"Error deleting grade: {e}")
            raise ValidationError("Grade not found.")
    
    @staticmethod
    def get_student_grades(student_id: int) -> list:
        """
        Get all grades for a specific student.
        """
        try:
            student = User.objects.get(id=student_id)
            grades = Grade.objects.filter(student=student)
            return list(grades)
        
        except ObjectDoesNotExist as e:
            logger.error(f"Error fetching grades for student: {e}")
            raise ValidationError("Student not found.")
    
    @staticmethod
    def get_assignment_grades(assignment_id: int) -> list:
        """
        Get all grades for a specific assignment.
        """
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            grades = Grade.objects.filter(assignment=assignment)
            return list(grades)
        
        except ObjectDoesNotExist as e:
            logger.error(f"Error fetching grades for assignment: {e}")
            raise ValidationError("Assignment not found.")