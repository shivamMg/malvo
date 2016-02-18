from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Question, Choice
from .dump_mcqs import dump_mcqs_to_file

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'mcqs/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.order_by('question_no')


# @login_required
def mcq(request):
    dump_mcqs_to_file()
    return render(request, 'mcqs/mcq_on_json.html')


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
            return HttpResponseRedirect(reverse('mcqs:mcq', args=(
                question.question_no + 1,
            )))
