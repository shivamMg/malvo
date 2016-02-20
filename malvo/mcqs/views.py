from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question
from .dump_mcqs import dump_mcqs_to_file
from teams.models import Team, TeamMcqAnswer


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'mcqs/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.order_by('question_no')


# @login_required
def mcq(request):
    dump_mcqs_to_file()
    return render(request, 'mcqs/mcq_on_json.html')


def answer(request):
    if request.method == 'POST':
        question_count = Question.objects.count()
        # Get Team object from logged-in team
        team = Team.objects.get(team_name=request.user)

        # Save answers for the Team
        for qno in range(1, question_count+1):
            answer = TeamMcqAnswer(
                question_no=qno,
                choice_text=request.POST.get(str(qno)),
                team=team
            )
            answer.save()
        return HttpResponseRedirect(reverse('mcqs:index'))
    else:
        return HttpResponseRedirect(reverse('mcqs:index'))
