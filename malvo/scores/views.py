from operator import itemgetter

from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

from teams.models import Team
from mcqs.models import Question as McqQuestion
from coding.models import InputCase, Question as CodingQuestion


def _get_team_mcq_score(team):
    score = 0

    for ans in team.teammcqanswer_set.all():
        question = McqQuestion.objects.get(question_no=ans.question_no,
                                           language=team.lang_pref)
        if ans.choice_no == question.answer_choice_no:
            score += 1

    return score


def _get_team_coding_score(team):
    score = 0

    for ans in team.teamcodinganswer_set.all():
        question = CodingQuestion.objects.get(question_no=ans.question_no)
        try:
            inputcase = question.inputcase_set.get(case_no=ans.inputcase_no)

            if ans.output_text == inputcase.answer_case_text:
                score += inputcase.points
        except InputCase.DoesNotExist:
            pass

    return score


def index(request):
    return render(request, 'scores/index.html', {
        'team_count': Team.objects.count(),}
    )


def leaderboard(request, app):
    team_list = []

    if app == 'mcqs':
        for team in Team.objects.all():
            team_list.append({
                'name': team.team_name,
                'score': _get_team_mcq_score(team),}
            )
        round_name = 'MCQs'
    elif app == 'coding':
        for team in Team.objects.all():
            team_list.append({
                'name': team.team_name,
                'score': _get_team_coding_score(team),}
            )
        round_name = 'Programming Challenges'

    team_list = sorted(team_list, key=itemgetter('score'), reverse=True)

    return render(request, 'scores/leaderboard.html', {
        'team_list': team_list,
        'round_name': round_name,}
    )
