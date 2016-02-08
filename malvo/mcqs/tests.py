from django.test import TestCase

from .models import Question


class QuestionMethodTests(TestCase):

    def test_default_question_no_for_new_question(self):
        """
        incre_question_count() should return the number of questions
        incremented by one
        """
        number_of_questions = Question.objects.count()
        if number_of_questions == None:
            count = 0
        else:
            count = number_of_questions
        incremented_count = count + 1
        self.assertEqual(Question.incre_question_count(), incremented_count)
