from operator import itemgetter

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from teams.models import Team
from mcqs.models import Question as McqQuestion
from coding.models import InputCase, Question as CodingQuestion


def _get_team_mcq_score(team):
    score, evaluated_list = 0, []

    for ans in team.teammcqanswer_set.all():
        question = McqQuestion.objects.get(question_no=ans.question_no,
                                           language=team.lang_pref)

        answer_choice = question.choice_set.get(
                choice_no=question.answer_choice_no).choice_text
        selected_choice = question.choice_set.get(
                choice_no=ans.choice_no).choice_text

        evaluated_list.append({
            'question_no': question.question_no,
            'answer_choice': answer_choice,
            'selected_choice': selected_choice,}
        )

        if ans.choice_no == question.answer_choice_no:
            score += 1

    evaluated_list = sorted(evaluated_list, key=itemgetter('question_no'))

    return (score, evaluated_list)


def _get_team_coding_score(team):
    score, evaluated_list = 0, []

    for ans in team.teamcodinganswer_set.all():
        question = CodingQuestion.objects.get(question_no=ans.question_no)
        try:
            inputcase = question.inputcase_set.get(case_no=ans.inputcase_no)

            evaluated_list.append({
                'question_no': question.question_no,
                'inputcase_no': inputcase.case_no,
                'correct_output': inputcase.answer_case_text,
                'answered_output': ans.output_text,
                'points': inputcase.points,}
            )

            if ans.output_text == inputcase.answer_case_text:
                score += inputcase.points
        except InputCase.DoesNotExist:
            pass

    evaluated_list = sorted(evaluated_list, key=itemgetter('question_no'))

    return (score, evaluated_list)


@user_passes_test(lambda u: u.is_admin)
def index(request):
    team_list = []

    for team in Team.objects.all():
        member_list = []
        for member in team.teammember_set.all():
            if member.full_name != '':
                member_list.append({
                    'full_name': member.full_name,
                    'email': member.email,
                    'mobile_no': member.mobile_no,}
                )

        team_list.append({
            'team_name': team.team_name,
            'member_list': member_list,
            'lang_pref': team.lang_pref,}
        )

    return render(request, 'scores/index.html', {
        'team_list': team_list,
        'team_count': Team.objects.count(),
        'mcqs_count': McqQuestion.objects.count(),
        'coding_count': CodingQuestion.objects.count(),
        'inputcase_count': InputCase.objects.count(),}
    )


@user_passes_test(lambda u: u.is_admin)
def leaderboard(request, app):
    team_list = []

    if app == 'mcqs':
        for team in Team.objects.all():
            team_list.append({
                'name': team.team_name,
                'score': _get_team_mcq_score(team)[0],}
            )
        round_name = 'MCQs'
    elif app == 'coding':
        for team in Team.objects.all():
            team_list.append({
                'name': team.team_name,
                'score': _get_team_coding_score(team)[0],}
            )
        round_name = 'Programming Challenges'

    team_list = sorted(team_list, key=itemgetter('score'), reverse=True)

    return render(request, 'scores/leaderboard.html', {
        'team_list': team_list,
        'round_name': round_name,}
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def evaluate(request, team_name, app):
    team = get_object_or_404(Team, team_name=team_name)

    if app == 'mcqs':
        score, evaluated_list = _get_team_mcq_score(team)
        template_name = 'scores/evaluate_mcqs.html'
    elif app == 'coding':
        score, evaluated_list = _get_team_coding_score(team)
        template_name = 'scores/evaluate_coding.html'

    return render(request, template_name, {
        'team_name': team.team_name,
        'evaluated_list': evaluated_list,
        'score': score,}
    )
