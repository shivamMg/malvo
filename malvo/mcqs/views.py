import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Question
from .dump_mcqs import dump_mcqs_to_file, JAVA_FILENAME, C_FILENAME
from teams.models import Team, TeamMcqAnswer


def team_and_question_list(team_name):
    """
    Returns Team object for `team_name` and questions list as per
    team language preference
    """
    team = Team.objects.get(team_name=team_name)
    questions = Question.objects.filter(language=team.lang_pref)
    return (team, questions)


@login_required
def index(request):
    team, questions = team_and_question_list(request.user)

    # Previous answers given by team
    answer_list = team.teammcqanswer_set.order_by('question_no')

    # Store key-value pairs of question numbers and answer statuses
    # If answer is empty, status is 'Unsolved', else 'Solved'
    answer_status_dict = {}

    # If no answers provided, mark all 'Unsolved'
    if not answer_list:
        answer_status_dict = {
            qno: 'Unsolved' for qno in range(1, questions.count()+1)}
    else:
        for ans in answer_list:
            if ans.choice_text == '':
                answer_status_dict[ans.question_no] = 'Unsolved'
            else:
                answer_status_dict[ans.question_no] = 'Solved'

    question_list = []
    for ques in questions.order_by('question_no'):
        qno = ques.question_no
        ques.status = answer_status_dict[qno]
        question_list.append(ques)

    return render(request, 'mcqs/index.html', {
        'question_list': question_list}
    )


@login_required
def mcq(request):
    team, questions = team_and_question_list(request.user)
    dump_mcqs_to_file()

    # Store key-value pairs of question numbers and answered choices
    # Both keys and values are strings
    answers = {}

    if team.teammcqanswer_set.exists():
        for answer in team.teammcqanswer_set.all():
            answers[str(answer.question_no)] = answer.choice_text
    # If no questions were answered previously, choices are marked empty strings
    else:
        answers = {str(i): "" for i in range(1, questions.count()+1)}

    if team.lang_pref == 'J':
        mcq_filename = JAVA_FILENAME
    else:
        mcq_filename = C_FILENAME

    return render(request, 'mcqs/mcq_on_json.html', {
        'previous_answers': json.dumps(answers,),
        'mcq_filename': mcq_filename,}
    )


@login_required
def answer(request):
    if request.method == 'POST':
        team, questions = team_and_question_list(request.user)

        # Check if team has answered questions before
        # If yes, delete all of them
        if team.teammcqanswer_set.exists():
            team.teammcqanswer_set.all().delete()

        # Save new answers
        for qno in range(1, questions.count()+1):
            choice_text = request.POST.get(str(qno))

            TeamMcqAnswer.objects.create(
                question_no=qno,
                choice_text=choice_text,
                team=team
            )

    return HttpResponseRedirect(reverse('mcqs:index'))
