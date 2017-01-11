# Older views. No longer required.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Question, Choice


class McqView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'mcqs/mcq.html'


@login_required
def answer(request, question_no):
    question_count = Question.objects.count()
    question = get_object_or_404(Question, question_no=question_no)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(selected_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'mcqs/mcq.html', {
            'question': question,
            'error_message': 'No option selected',
        })
    else:
        # if it's the last question, redirect to index page
        # else redirect to next question
        if question.question_no == question_count:
            return HttpResponseRedirect(reverse('mcqs:index'))
        else:
            return HttpResponseRedirect(reverse('mcqs:questions', args=(
                question.question_no + 1,
            )))
