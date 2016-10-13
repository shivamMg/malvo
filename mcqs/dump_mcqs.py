import json

from django.core.cache import cache

from .models import Question


def extract_mcqs(lang_code):
    """
    Returns JSON dump of all Questions and their Choices for a language
    """
    data = []
    for ques in Question.objects.filter(language=lang_code):
        choice_list = []
        # Extract choices
        for choice in ques.choice_set.all():
            choice_list.append({
                'no': choice.choice_no,
                'text': choice.choice_text,}
            )

        data.append({
            'qno': ques.question_no,
            'qtext': ques.question_text,
            'choices': choice_list,}
        )

    return json.dumps(data)


def set_mcqs_in_cache():
    """
    Set MCQs in cache if they have changed or have not been set.
    """
    languages = {
        'C': 'c_mcqs',
        'J': 'java_mcqs',
    }

    # If MCQs have been changed or have not been created
    if not cache.get('mcqs_flag', False):
        for lang_code, cache_key in languages.items():
            mcqs_json = extract_mcqs(lang_code)
            cache.set(cache_key, mcqs_json)

        # Mark MCQs as unchanged
        cache.set('mcqs_flag', True)
