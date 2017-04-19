import json
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Question
from .dump_mcqs import set_mcqs_in_cache
from teams.models import Team, TeamMcqAnswer


def _team_and_question_list(team_name):
    """
    Returns Team object for `team_name` and questions list as per
    team language preference
    """
    team = Team.objects.get(team_name=team_name)
    question_list = Question.objects.filter(language=team.lang_pref)
    return (team, question_list)


def _get_question_statuses(team):
    """
    Returns a dictionary of Question numbers and statuses as key-value pairs.
    Status could be:
        'S': Solved
        'U': Unattempted
    """
    status_dict = {}

    for ques in Question.objects.filter(language=team.lang_pref):
        try:
            team.teammcqanswer_set.get(question_no=ques.question_no)
            status = 'S'
        except TeamMcqAnswer.DoesNotExist:
            status = 'U'

        status_dict[ques.question_no] = status

    return status_dict


@login_required
def index(request):
    team = Team.objects.get(team_name=request.user)
    status_dict = _get_question_statuses(team)
    ordered_status_dict = OrderedDict(sorted(status_dict.items()))

    return render(request, 'mcqs/index.html', {
        'remaining_time': team.remaining_mcqs_time,
        'has_started': bool(team.mcqs_start_time is not None),
        'status_dict': ordered_status_dict
    })


@login_required
def questions(request):
    team = Team.objects.get(team_name=request.user)
    set_mcqs_in_cache()

    # Save current time if `mcqs_start_time` is NULL in db
    if team.mcqs_start_time is None:
        team.mcqs_start_time = timezone.now()
        team.save()

    if team.is_mcqs_time_over:
        return HttpResponseRedirect(reverse('mcqs:index'))

    answer_dict = {}

    for ans in team.teammcqanswer_set.all():
        answer_dict[str(ans.question_no)] = ans.choice_no

    if team.lang_pref == 'J':
        cache_key = 'java_mcqs'
    else:
        cache_key = 'c_mcqs'

    return render(request, 'mcqs/questions.html', {
        'remaining_time': team.remaining_mcqs_time,
        'previous_answers': json.dumps(answer_dict),
        'mcqs': cache.get(cache_key),
    })


@login_required
def answer(request):
    # Check for Time over has intentionally been ignored

    if request.method == 'POST':
        team, question_list = _team_and_question_list(request.user)

        for ques in question_list:
            choice_no = request.POST.get(str(ques.question_no), False)

            if choice_no:
                obj, is_created = TeamMcqAnswer.objects.update_or_create(
                    question_no=ques.question_no,
                    team=team,
                    defaults={'choice_no': choice_no})

    return HttpResponse({'status': 'ok'})
