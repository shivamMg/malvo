from django.db import models


class Question(models.Model):
    """
    Coding challenge question
    """
    question_no = models.IntegerField(unique=True)
    question_text = models.TextField()

    def __str__(self):
        return "Q{}. {}".format(self.question_no, self.question_text[:80])


class InputCase(models.Model):
    """
    Input case for a Question
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    case_no = models.IntegerField(default=0)
    case_text = models.TextField()
    answer_case_text = models.TextField()
    points = models.IntegerField(default=1)

    class Meta:
        unique_together = ('question', 'case_no',)

    def __str__(self):
        return self.case_text
