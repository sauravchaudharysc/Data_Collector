from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Problem, Submission, Criteria, Rating, GradingHistory
from django.utils import timezone
from rest_framework import status
import json

def home(request):
    return HttpResponse("Welcome to Data Collector")

def dummy(id):
    reverse_id = id[::-1]
    return reverse_id

class DataPoint(APIView):
    """
    An API view to handle GET and POST requests.
    """

    def get(self, request, format=None):
        # Write Logic for handling GET requests
        data = {'message': 'GET request received'}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:    
            data = request.data # Extract the data from the request\
            data = data['0']
            user_id = data['user_id']
            for lab_name in data.keys():
                lab_id = lab_name
                for program_activity in data[lab_name].keys():
                    #Extract Program Activity ID
                    problem_id = program_activity

                    #Extract Problem Statement    
                    problem_statement = data[lab_name][program_activity]['problem_statement']
                    
                    filename = data[lab_name][program_activity]['file_name'] # Filename

                    #Create Problem Object
                    problem, created = Problem.objects.get_or_create(
                        problem_id=problem_id,
                        defaults={
                            'problem_statement': problem_statement,
                            'user_id': user_id
                            'lab_id': lab_id
                        }
                    )

                    # Create Criteria and Rating objects
                    criterions=data[lab_name][program_activity]['rubric']
                    for criteria in criterions:
                        for criter_id,criter in criteria.items():
                            criter_title = criter['title']
                            criter_description = criter['description']
                            criteria_object, _ = Criteria.objects.get_or_create(
                                id=criter_id,
                                defaults={
                                    'title': criter_title,
                                    'description': criter_description,
                                    'problem_id': problem_id
                                }
                            )
                            #Create Rating Details Object First and associate with Criteria
                            for rating_id,rating_data in criter['ratings'].items():
                                rating_title = rating_data['title']
                                rating_description = rating_data['description']
                                rating_marks = rating_data.get('marks', 0)  # Use default 0 if not provided

                                rating_obj = Rating.objects.get_or_create(
                                    id=rating_id,
                                    defaults={
                                        'title': rating_title,
                                        'description': rating_description,
                                        'marks': rating_marks,
                                        'criteria_id': criter_id
                                    }
                                )
                    
                    for student_id in data[lab_name][program_activity]['student_submissions'].keys():
                        student_id=student_id # Student ID
                        dummy_id = dummy(student_id) # Dummy ID
                        student_submission_details = data[lab_name][program_activity]['student_submissions'][student_id]
                        source_code = student_submission_details['source_code'] # Source Code
                        
                        # Create Submission object
                        submission = Submission.objects.create(
                            problem_id=problem_id,
                            student_id=student_id,
                            dummy_id=dummy_id,
                            filename=filename,
                            source_code=source_code
                        )

                        for criteria_id in student_submission_details['manual_rating'].keys():
                            # Fetch the Criteria object based on problem_id and criteria_id
                            fetch_criteria = Criteria.objects.filter(problem_id=problem_id, criteria_id=criteria_id).first()
                            
                            if fetch_criteria:
                                # Extract manual rating and comments from the student_submission_details
                                manual_rating, manual_comments = student_submission_details['manual_rating'].get(criteria_id, [None, None])
                                
                                # Extract AI rating and comments from the student_submission_details
                                ai_rating, ai_comments = student_submission_details['ai_rating'].get(criteria_id, [None, None])
                                
                                # Check if a GradingHistory object with the same problem_id, student_id, and criteria exists
                                existing_entry = GradingHistory.objects.filter(
                                    problem_id=problem_id,
                                    student_id=student_id,
                                    criteria=fetch_criteria  # Using the Criteria instance directly
                                )
                                
                                if not existing_entry:
                                    # Create a new GradingHistory object if no existing entry was found
                                    grading_history = GradingHistory.objects.create(
                                        problem_id=problem_id,
                                        student_id=student_id,
                                        dummy_id=dummy_id,
                                        submission=submission,
                                        criteria=fetch_criteria,  # Using the Criteria instance directly
                                        manual_rating=manual_rating,
                                        ai_rating=ai_rating,
                                        manual_comments=manual_comments,
                                        ai_comments=ai_comments
                                    )
                                else:
                                    print(f"Entry already exists for problem_id={problem_id}, student_id={student_id}, criteria_id={criteria_id}")
                            else:
                                print(f"Criteria with ID {criteria_id} not found for problem_id={problem_id}")
                      
            return Response({"message": "Data received", "data": data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"error": "An error occurred"}, status=status.HTTP_400_BAD_REQUEST)
       