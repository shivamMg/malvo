import os
import json

from .models import Question


def extract_mcqs():
    """
    Returns JSON dump of all Questions and their Choices
    """
    data = []
    for question in Question.objects.all():
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
    filename = 'mcq_dump.json'
    filepath = os.path.join(base_dir, 'static', 'mcqs', filename)

    # If mcqs json file does not exist
    if not os.path.isfile(filepath):
        data = extract_mcqs()
        with open(filepath, 'w') as json_file:
            json_file.write(data)
