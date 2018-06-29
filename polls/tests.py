from models import Choice, Question
from django.utils import timezone

if __name__ == '__main__':
    q = Question(question_text='How long have you been married?',
                 pub_date=timezone.now())


    # Save the object into the database.
    q.save()
