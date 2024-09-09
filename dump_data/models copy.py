from django.db import models

class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    problem_statement = models.TextField(default="No problem statement provided.")
    user_id = models.CharField(max_length=255, default="Unknown User ID")
    lab_id = models.IntegerField(required=True)
    def __str__(self):
        return f"Problem {self.problem_id}: {self.problem_statement[:30]}... created by {self.user_id}"   

class Submission(models.Model):
    id = models.IntegerField(primary_key=True)
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255, default="Unknown Student ID")
    dummy_id = models.CharField(max_length=255, default="Unknown Dummy ID")
    filename = models.CharField(max_length=255, default="default_filename.cpp")
    source_code = models.TextField(default="No source code provided.")
    def __str__(self):
        return f"Submission {self.filename}: {self.source_code}"
    def __repr__(self):
        return f"<Submission(id={self.id}, name='{self.filename}', description='{self.source_code}')>"

class Criteria(models.Model):
    id = models.IntegerField(primary_key=True)
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Default Criterion Title")
    description = models.TextField(default="No description provided.")

class Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, default="Default Title")
    description = models.TextField(default="No description provided.")
    marks = models.IntegerField(default=0)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    def __str__(self):
        pass

    def __str__(self):
        return f"Criteria {self.title}: Linked to Rating"
    
    def descriptive_info(self):
        return (f"Problem ID: {self.problem_id}, Title: '{self.title}', "
                f"Description: '{self.description}', ")

class GradingHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    manual_rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    ai_rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    manual_comments = models.TextField(default="No comments.")
    ai_comments = models.TextField(default="No AI reasonings.")
    