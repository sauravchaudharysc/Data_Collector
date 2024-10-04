from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import Prefetch
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../data_collector.settings') 
django.setup()

from dump_data.models import GradingHistory, Problem, Criteria, Rating, Submission

class Command(BaseCommand):
    """Django Command to handle grading history, problem, or criteria"""
    help = 'Handles grading history, problem, or criteria'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--option', type=str, help='Defines the operation')

    def handle_grading_history(self):
        """Handle grading history operation"""
        
        # Fetch The Problem Statement
        try:
            # problem_id = int(input("Enter the ID of the problem you want to see: "))
            problem_id = 49
            problem = Problem.objects.get(id=problem_id)
            problemStatement=problem.problem_statement
        except Problem.DoesNotExist:
            print(f"No problem found with ID: {problem_id}")

        print(problemStatement)



        # Fetch all Submissions for the given problem
        submissions = Submission.objects.filter(problem_id=problem_id)

        studentSubmissions={}
        for submission in submissions:
            studentSubmissions[submission.student_id]=submission.source_code
        
        print(studentSubmissions)


        # Fetch the Rubrics for the given problem
        rubrics={}
        try:
            # Fetch all criteria for the given problem, including their associated ratings
            criteria_with_ratings = Criteria.objects.filter(problem_id=problem_id).prefetch_related('rating_set')
            
            for criteria in criteria_with_ratings:
                criteriaDict={}
                criteriaDict['description']=criteria.description
                ratingsDict={}
                ratings = criteria.rating_set.all()
                if ratings.exists():
                    for rating in ratings:
                        ratingsDict[rating.title]=rating.description
                else:
                    print("  No ratings available for this criteria.")
                criteriaDict['ratings']=ratingsDict
                rubrics[criteria.title]=criteriaDict
        except Problem.DoesNotExist:
            print(f"No problem found with ID: {problem_id}")

        print(rubrics)


        
        # Fetch the Original Grades for the given problem
        grades = {}
        submissions = Submission.objects.filter(problem_id=problem_id)

        for submission in submissions:
            grading_histories = GradingHistory.objects.filter(submission=submission.id)
            
            for grading_history in grading_histories:
                criterion_title = grading_history.criteria.title
                student_id = submission.student_id
                try:
                    manual_marks=grading_history.manual_rating.title
                except GradingHistory.manual_rating.RelatedObjectDoesNotExist:
                    print("Manual Rating: Not present")
                    continue
                
                # Initialize the nested dictionary for each criterion title if it doesn't exist
                if criterion_title not in grades:
                    grades[criterion_title] = {}

                # Store the student_id as the key and manual_rating.marks as the value
                grades[criterion_title][student_id] = manual_marks
        print(grades)
        
    def handle_problem_statement(self):
        """Handle problem operation"""
        # Fetch all problem ids and problem statements
        problems = Problem.objects.values_list('id', 'problem_statement')
        
        # Uncomment Below To Print all problems along with ID
        # for problem_id, problem_statement in problems:
        #     print(f"ID: {problem_id}, Problem Statement: {problem_statement[:50]}...")  # Print a truncated statement
        
        # User input
        try:
            # problem_id = int(input("Enter the ID of the problem you want to see: "))
            problem_id = 49
            problem = Problem.objects.get(id=problem_id)
            print(f"Problem Statement for ID {problem_id}: {problem.problem_statement}")
        except Problem.DoesNotExist:
            print(f"No problem found with ID: {problem_id}")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

            
    def handle_criteria(self):
        """Handle criteria operation"""
        pass  # Replace this with actual implementation

    def handle_criteria_with_ratings(self):
        try:
            problem_id=49
            
            # Fetch all criteria for the given problem, including their associated ratings
            criteria_with_ratings = Criteria.objects.filter(problem_id=problem_id).prefetch_related('rating_set')
            
            for criteria in criteria_with_ratings:
                print(f"Criteria: {criteria.title} (ID: {criteria.id}) (Description: {criteria.description}")
                ratings = criteria.rating_set.all()
                if ratings.exists():
                    for rating in ratings:
                        print(f"  Rating: {rating.title}, Marks: {rating.marks}, Description: {rating.description}")
                else:
                    print("  No ratings available for this criteria.")
            
        except Problem.DoesNotExist:
            print(f"No problem found with ID: {problem_id}")

    def handle_submissions_by_problem(self):
        # Prefetch the grading history to reduce the number of queries
        problem_id = 49
        submissions = Submission.objects.filter(problem_id=problem_id)

        for submission in submissions:
            grading_histories = GradingHistory.objects.filter(submission=submission.id)
            for grading_history in grading_histories:
                print(f"Grading History ID: {grading_history.id}")
                print(f"Criteria: {grading_history.criteria}")
                print(submission)
                # Check for manual rating
                try:
                    print(f"Manual Rating: {grading_history.manual_rating}")
                except GradingHistory.manual_rating.RelatedObjectDoesNotExist:
                    print("Manual Rating: Not present")
                
                # Check for manual comments
                try:
                    print(f"Manual Comments: {grading_history.manual_comments}")
                except GradingHistory.manual_comments.RelatedObjectDoesNotExist:
                    print("Manual Comments: Not present")
                
                # Check for AI rating
                try:
                    print(f"AI Rating: {grading_history.ai_rating}")
                except GradingHistory.ai_rating.RelatedObjectDoesNotExist:
                    print("AI Rating: Not present")
                
                # Check for AI comments
                try:
                    print(f"AI Comments: {grading_history.ai_comments}")
                except GradingHistory.ai_comments.RelatedObjectDoesNotExist:
                    print("AI Comments: Not present")
                
                print("-" * 30)  

    def start_process(self, option=None):
        """Handle the selected option"""
        if option == '1':
            self.handle_grading_history()
        elif option == '2':
            self.handle_problem_statement()
        elif option == '3':
            self.handle_criteria_with_ratings()
        elif option == '4':
            self.handle_submissions_by_problem()
        else:
            self.stdout.write("Sorry, wrong option")

    def handle(self, *args, **kwargs):
        option = kwargs.get('option')

        if option:
            self.stdout.write('------------------------------------------------------')
            self.start_process(option=option)
            self.stdout.write("------------------------------------------------------")
        else:
            while True:
                self.stdout.write('Choose the option:')
                self.stdout.write('1. Grading History')
                self.stdout.write('2. Problem Statement')
                self.stdout.write('3. Criteria Along With Ratings')
                self.stdout.write('4. Student Submission Along With Ratings')
                self.stdout.write('5. Exit')
                option = input('Enter the option: ')
                self.stdout.write('------------------------------------------------------')
                if option == '5':
                    self.stdout.write("Exiting...")
                    break
                self.start_process(option=option)
                self.stdout.write("------------------------------------------------------")