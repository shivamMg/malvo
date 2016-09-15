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
    answer_choice_no = models.IntegerField(default=0)

    class Meta:
        unique_together = ('language', 'question_no',)

    def __str__(self):
        return "Q{}. [{}] {}".format(self.question_no, self.language,
                                    self.question_text[:80])


class Choice(models.Model):
    """Choice tied to a Question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_no = models.IntegerField(default=0)
    choice_text = models.CharField(max_length=1000)

    class Meta:
        unique_together = ('question', 'choice_no',)

    def __str__(self):
        return self.choice_text
