import os
import json

from .models import Question

JAVA_FILENAME = 'java_mcq_dump.json'
C_FILENAME = 'c_mcq_dump.json'


def extract_mcqs(lang_code):
    """
    Returns JSON dump of all Questions and their Choices
    """
    data = []
    for question in Question.objects.filter(language=lang_code):
        choices = []
        # Extract choices
        for choice in question.choice_set.all():
            choices.append(choice.choice_text)

        data.append({
            'qno': question.question_no,
            'qtext': question.question_text,
            'choices': choices}
        )
    return json.dumps(data)


def dump_mcqs_to_file():
    """
    Writes to MCQs JSON file in `static/mcqs` directory, if it does not exist.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    java_filepath = os.path.join(base_dir, 'static', 'mcqs', JAVA_FILENAME)
    c_filepath = os.path.join(base_dir, 'static', 'mcqs', C_FILENAME)

    lang_files = {
        'J': java_filepath,
        'C': c_filepath,
    }

    for lang_code, filepath in lang_files.items():
        if not os.path.isfile(filepath):
            data = extract_mcqs(lang_code)
            with open(filepath, 'w') as json_file:
                json_file.write(data)
