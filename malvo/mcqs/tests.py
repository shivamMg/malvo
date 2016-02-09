from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question


class QuestionModelTests(TestCase):
    """Tests for models"""
    def test_default_question_number_for_new_question(self):
        """
        `incre_question_count()` should return the total number of questions
        incremented by one.
        """
        number_of_questions = Question.objects.count()
        if number_of_questions == None:
            count = 0
        else:
            count = number_of_questions
        incremented_count = count + 1
        self.assertEqual(Question.incre_question_count(), incremented_count)


def create_question(question_text, choice_list):
    """
    Create question with `question_text` and with choices in `choice_list`.
    """
    question = Question.objects.create(question_text=question_text)
    for choice in choice_list:
        question.choice_set.create(choice_text=choice)
    return question


class QuestionViewTests(TestCase):
    """Tests for views"""
    def test_index_view_with_no_mcqs(self):
        """
        If no mcq exists, a message should be displayed.
        """
        response = self.client.get(reverse('mcqs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No MCQs available")
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_mcq_view_with_no_choices(self):
        """
        If choices for an mcq do not exist, a message should be displayed.
        """
        # Create question without choices
        question = create_question("A nice and healthy question text. Is it?", [])
        response = self.client.get(reverse('mcqs:mcq', args=(
            question.question_no,
        )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No choices available")

    def test_answer_view_with_no_option_selected(self):
        """
        If no option is selected as an answer, display an error message.
        """
        question = create_question("Dummy question, is it?", [
            "Yes it is",
            "Nope, it is genuine",
        ])
        response = self.client.post(reverse('mcqs:answer', args=(
            question.question_no,
        )), {})
        self.assertEqual(response.context['error_message'],
                         "No option selected")

    def test_answer_view_for_redirection_to_next_question(self):
        """
        If a question is answered, redirect to next question.
        """
        question_one = create_question("Dummy question, is it?", [
            "Yes it is",
            "Nope, it is genuine",
        ])
        create_question("Dummy question, is it?", [
            "Yes it is",
            "Nope, it is genuine",
        ])
        response = self.client.post(reverse('mcqs:answer', args=(
            question_one.question_no,
        )), {'choice': 1})
        self.assertRedirects(response, '/mcqs/2/')

    def test_answer_view_for_redirection_to_index(self):
        """
        If the question answered is the last question, redirect to index.
        """
        question = create_question("Dummy question, is it?", [
            "Yes it is",
            "Nope, it is genuine",
        ])
        response = self.client.post(reverse('mcqs:answer', args=(
            question.question_no,
        )), {'choice': 1})
        self.assertRedirects(response, '/mcqs/')
