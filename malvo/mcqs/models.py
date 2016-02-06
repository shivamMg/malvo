from django.db import models


class Question(models.Model):
    """MCQ Question with question number and text"""
    def incre_question_count():
        """Return incremented question count"""
        count = Question.objects.count()
        if count == None:
            count = 0
        return count + 1

    question_no = models.IntegerField(unique=True, default=incre_question_count)
    question_text = models.TextField()

    def __str__(self):
        return "Q{0}. {1}".format(self.question_no, self.question_text)


class Choice(models.Model):
    """Choice tied to a Question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.choice_text
