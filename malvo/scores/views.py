from operator import itemgetter

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from teams.models import Team, TeamCodingAnswer, TeamMcqAnswer
from mcqs.models import Question as McqQuestion
from coding.models import InputCase, Question as CodingQuestion


def _get_team_mcq_score(team):
    score, evaluated_list = 0, []

    for ques in McqQuestion.objects.filter(language=team.lang_pref):
        try:
            answer = team.teammcqanswer_set.get(question_no=ques.question_no)
            selected_choice = ques.choice_set.get(
                    choice_no=answer.choice_no).choice_text

            if answer.choice_no == ques.answer_choice_no:
                score += 1
        except TeamMcqAnswer.DoesNotExist:
            selected_choice = ''

        correct_choice = ques.choice_set.get(
                choice_no=ques.answer_choice_no).choice_text

        evaluated_list.append({
            'question_no': ques.question_no,
            'correct_choice': correct_choice,
            'selected_choice': selected_choice,}
        )

    evaluated_list = sorted(evaluated_list, key=itemgetter('question_no'))

    return (score, evaluated_list)


def _get_team_coding_score(team):
    score, evaluated_list = 0, []

    for ques in CodingQuestion.objects.all():
        inputcase_list = []
        for inputcase in ques.inputcase_set.all():
            try:
                answer = team.teamcodinganswer_set.get(
                            question_no=ques.question_no,
                            inputcase_no=inputcase.case_no)
                output_text = answer.output_text

                if answer.output_text == inputcase.answer_case_text:
                    score += inputcase.points

            except TeamCodingAnswer.DoesNotExist:
                output_text = ''

            inputcase_list.append({
                'inputcase_no': inputcase.case_no,
                'correct_output': inputcase.answer_case_text,
                'answered_output': output_text,
                'points': inputcase.points,}
            )

        evaluated_list.append({
            'question_no': ques.question_no,
            'inputcase_list': inputcase_list,}
        )

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
        'team_lang_pref': team.get_lang_pref_name(),
        'evaluated_list': evaluated_list,
        'score': score,}
    )
