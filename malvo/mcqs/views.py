import json

from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Question
from .dump_mcqs import dump_mcqs_to_file, JAVA_FILENAME, C_FILENAME
from teams.models import Team, TeamMcqAnswer


def _team_and_question_list(team_name):
    """
    Returns Team object for `team_name` and questions list as per
    team language preference
    """
    team = Team.objects.get(team_name=team_name)
    question_list = get_list_or_404(Question, language=team.lang_pref)
    return (team, question_list)


def _get_question_statuses(team):
    """
    Returns a dictionary of Question numbers and statuses as key-value pairs.
    Status could be:
        'S': Solved
        'U': Unattempted
    """
    status_dict = {}

    for ques in Question.objects.all():
        try:
            team.teammcqanswer_set.get(question_no=ques.question_no)
            status = 'S'
        except TeamMcqAnswer.DoesNotExist:
            status = 'U'

        status_dict[ques.question_no] = status

    return status_dict


@login_required
def index(request):
    team, question_list = _team_and_question_list(request.user)
    status_dict = _get_question_statuses(team)

    return render(request, 'mcqs/index.html', {'status_dict': status_dict,})


@login_required
def mcq(request):
    team, question_list = _team_and_question_list(request.user)
    dump_mcqs_to_file()

    answer_dict = {}

    for ans in team.teammcqanswer_set.all():
        answer_dict[str(ans.question_no)] = ans.choice_no

    if team.lang_pref == 'J':
        mcq_filename = JAVA_FILENAME
    else:
        mcq_filename = C_FILENAME

    return render(request, 'mcqs/mcq.html', {
        'previous_answers': json.dumps(answer_dict),
        'mcq_filename': mcq_filename,}
    )


@login_required
def answer(request):
    if request.method == 'POST':
        team, question_list = _team_and_question_list(request.user)

        for ques in question_list:
            choice_no = request.POST.get(str(ques.question_no), False)

            if choice_no:
                obj, is_created = TeamMcqAnswer.objects.update_or_create(
                    question_no=ques.question_no,
                    team=team,
                    defaults={'choice_no': choice_no,}
                )

    return HttpResponseRedirect(reverse('mcqs:index'))
