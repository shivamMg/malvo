from django.db import models


class Question(models.Model):
    """MCQ with question number, text and language type"""
    PROG_LANGS = (
        ('C', 'C'),
        ('J', 'Java'),
    )

    language = models.CharField(max_length=1, choices=PROG_LANGS)
    question_no = models.IntegerField()
    question_text = models.TextField()

    class Meta:
        unique_together = (('language', 'question_no'),)

    def __str__(self):
        return "Q{0}. {1}".format(self.question_no, self.question_text)


class Choice(models.Model):
    """Choice tied to a Question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.choice_text
