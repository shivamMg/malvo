from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Question
from teams.models import TeamCodingAnswer, Team


def get_case_list(question):
    """
    Returns a list of cases.
    case:
        input:
            case_no
            case_text
        output:
            case_no
            field_name
    """
    case_list = []

    for input_case in question.inputcase_set.all():
        case_list.append({
            'input': {
                'case_no': input_case.case_no,
                'case_text': input_case.case_text},
            'output': {
                'case_no': input_case.case_no,
                'field_name': 'output_field-' + str(input_case.case_no)}}
        )

    return case_list


@login_required
def index(request):
    # team = Team.objects.get(team_name=request.user)
    # answer_list = team.teamcodinganswer_set.order_by('question_no')

    question_list = []
    for ques in Question.objects.all():
        question_list.append({
            'question_no': ques.question_no,}
        )

    return render(request, 'coding/index.html', {
        'question_list': question_list,}
    )


@login_required
def challenge(request, question_no):
    question = get_object_or_404(Question, question_no=question_no)
    case_list = get_case_list(question)

    return render(request, 'coding/challenge.html', {
        'question': question,
        'case_list': case_list,}
    )


@login_required
@csrf_exempt
def answer(request, question_no):
    question = get_object_or_404(Question, question_no=question_no)

    if request.method == 'POST':
        team = Team.objects.get(team_name=request.user)
        case_list = get_case_list(question)

        for case in case_list:
            output_field = case['output']['field_name']
            output_text = request.POST.get(output_field)

            obj, is_created = TeamCodingAnswer.objects.update_or_create(
                question_no=question.question_no,
                input_case_no=case['input']['case_no'],
                team=team,
                defaults={'output_text': output_text,}
            )

    next_question_no = int(question_no) + 1
    if Question.objects.filter(question_no=next_question_no).exists():
        return HttpResponseRedirect(reverse('coding:challenge',
                                    args=(next_question_no,)))
    else:
        return HttpResponseRedirect(reverse('coding:index'))
