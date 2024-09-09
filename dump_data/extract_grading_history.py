import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_collector.settings')  # Replace 'your_project.settings' with your settings module
django.setup()

from dump_data.models import GradingHistory 

def extract_grading_history(problem_id=None, student_id=None):
    # Build a query based on provided filters
    filters = {}
    if problem_id:
        filters['problem_id'] = problem_id
    if student_id:
        filters['student_id'] = student_id
    
    # Fetch filtered GradingHistory records
    grading_histories = GradingHistory.objects.filter(**filters)
    
    for grading_history in grading_histories:
        print(f"GradingHistory ID: {grading_history.id}")
        print(f"Problem ID: {grading_history.problem_id}")
        print(f"Student ID: {grading_history.student_id}")
        print(f"Dummy ID: {grading_history.dummy_id}")
        print(f"Submission: {grading_history.submission.filename}")
        print(f"Criteria: {grading_history.criteria.title}")
        print(f"Manual Rating: {grading_history.manual_rating}")
        print(f"AI Rating: {grading_history.ai_rating}")
        print(f"Manual Comments: {grading_history.manual_comments}")
        print(f"AI Comments: {grading_history.ai_comments}")
        print("-" * 40)
