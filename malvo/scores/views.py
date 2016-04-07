from operator import itemgetter

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from teams.models import Team, TeamCodingAnswer, TeamMcqAnswer, UploadFileModel
from mcqs.models import Question as McqQuestion
from coding.models import InputCase, Question as CodingQuestion


def _get_teaminfo_list():
    teaminfo_list = []

    for team in Team.objects.all():
        member_list = []
        for member in team.teammember_set.all():
            if member.full_name != '':
                member_list.append({
                    'full_name': member.full_name,
                    'college_id': member.college_id,
                    'email': member.email,
                    'mobile_no': member.mobile_no,}
                )

        teaminfo_list.append({
            'team_name': team.team_name,
            'member_list': member_list,
            'lang_pref': team.lang_pref,}
        )

    return teaminfo_list


def _get_mcq_score(team):
    score = 0

    for ans in team.teammcqanswer_set.all():
        question = McqQuestion.objects.get(question_no=ans.question_no,
                language=team.lang_pref)

        if ans.choice_no == question.answer_choice_no:
            score += 1

    return score


def _get_mcq_evaluation(team):
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


def _get_coding_score(team):
    score = 0

    for ans in team.teamcodinganswer_set.all():
        question = CodingQuestion.objects.get(question_no=ans.question_no)
        inputcase = InputCase.objects.get(question=question,
                case_no=ans.inputcase_no)

        if ans.output_text == inputcase.answer_case_text:
            score += inputcase.points

    return score


def _get_coding_evaluation(team):
    score, evaluated_list = 0, []

    for ques in CodingQuestion.objects.all():
        inputcase_list = []
        for inputcase in ques.inputcase_set.all():
            try:
                answer = team.teamcodinganswer_set.get(
                            question_no=ques.question_no,
                            inputcase_no=inputcase.case_no)
                output_text = answer.output_text

                # Do not include inputcase for empty answers
                if output_text == '':
                    continue

                if answer.output_text == inputcase.answer_case_text:
                    score += inputcase.points

                inputcase_list.append({
                    'inputcase_no': inputcase.case_no,
                    'correct_output': inputcase.answer_case_text,
                    'answered_output': output_text,
                    'points': inputcase.points,}
                )
            except TeamCodingAnswer.DoesNotExist:
                pass

        evaluated_list.append({
            'question_no': ques.question_no,
            'inputcase_list': inputcase_list,}
        )

    evaluated_list = sorted(evaluated_list, key=itemgetter('question_no'))

    return (score, evaluated_list)


@user_passes_test(lambda u: u.is_admin)
def index(request):

    return render(request, 'scores/index.html', {
        'team_list': _get_teaminfo_list,
        'team_count': Team.objects.count(),
        'mcqs_count': McqQuestion.objects.count(),
        'coding_count': CodingQuestion.objects.count(),
        'inputcase_count': InputCase.objects.count(),}
    )


@user_passes_test(lambda u: u.is_admin)
def leaderboard(request, app):
    teaminfo_list = _get_teaminfo_list()

    if app == 'mcqs':
        get_score_func = _get_mcq_score
    elif app == 'coding':
        get_score_func = _get_coding_score

    for teaminfo in teaminfo_list:
        team = Team.objects.get(team_name=teaminfo['team_name'])
        teaminfo['score'] = get_score_func(team)

    teaminfo_list = sorted(teaminfo_list, key=itemgetter('score'), reverse=True)

    return render(request, 'scores/leaderboard.html', {
        'team_list': teaminfo_list,
        'app': app,}
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def evaluate(request, team_name, app):
    team = get_object_or_404(Team, team_name=team_name)

    if app == 'mcqs':
        score, evaluated_list = _get_mcq_evaluation(team)
        template_name = 'scores/evaluate_mcqs.html'
    elif app == 'coding':
        score, evaluated_list = _get_coding_evaluation(team)
        template_name = 'scores/evaluate_coding.html'

    member_list = []
    for member in team.teammember_set.all():
        if member.full_name != '':
            member_list.append({
                'full_name': member.full_name,
                'college_id': member.college_id,
                'email': member.email,
                'mobile_no': member.mobile_no,}
            )

    return render(request, template_name, {
        'team_name': team.team_name,
        'member_list': member_list,
        'team_lang_pref': team.lang_pref,
        'evaluated_list': evaluated_list,
        'score': score,}
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def display_file(request, team_name, question_no):
    team = get_object_or_404(Team, team_name=team_name)
    uploaded_file = get_object_or_404(UploadFileModel, team=team,
                                      question_no=question_no)

    if team.lang_pref == 'C':
        language_class = 'c'
    else:
        language_class = 'java'

    return render(request, 'scores/file_display.html', {
        'question_no': question_no,
        'file_url': uploaded_file.file.url,
        'language_class': language_class,}
    )
