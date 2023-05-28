from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import HttpResponse
from quiz_api.models import Quiz
from django_redis import get_redis_connection

from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse


@ratelimit(key='user', rate='10/m', block=True)
@csrf_exempt
def create_quiz(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        options = request.POST.getlist('options[]')
        right_answer = request.POST.get('right_answer')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')


        # Check if the same quiz details already exist
        existing_quiz = Quiz.objects.filter(
            question=question,
            options=options,
            right_answer=right_answer,
            start_date=start_date,
            end_date=end_date
        ).exists()

        if existing_quiz:
            return JsonResponse({'message': 'Quiz already exists'})

        # Create the new quiz
        quiz = Quiz.objects.create(
            question=question,
            options=options,
            right_answer=right_answer,
            start_date=start_date,
            end_date=end_date
        )
        return JsonResponse({'message': 'Quiz created successfully!'})

    else:
        return JsonResponse({'error': 'Invalid request method'})


def get_active_quiz(request):
    current_time = timezone.localtime(timezone.now())

    quizzes = Quiz.objects.all()

    active_quizzes = []
    for quiz in quizzes:
        start_date = timezone.localtime(quiz.start_date)
        end_date = timezone.localtime(quiz.end_date)
        if start_date <= current_time <= end_date:
            quiz_data = {
                'question': quiz.question,
                'options': quiz.options,
                'start_date': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end_date': end_date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            active_quizzes.append(quiz_data)

    if active_quizzes:
        return JsonResponse({'quizzes': active_quizzes})
    else:
        return JsonResponse({'message': 'No active quizzes found'})


def get_quiz_result(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id, end_date__lt=timezone.now())
        return JsonResponse({'right_answer': quiz.right_answer})
    except Quiz.DoesNotExist:
        return JsonResponse({'message': 'Quiz result not available'})


def retrieve_all_quizzes(request):
    try:
        quizzes = Quiz.objects.all()
        all_quizzes = []
        for quiz in quizzes:
            start_date = timezone.localtime(quiz.start_date)
            end_date = timezone.localtime(quiz.end_date)
            quiz_data = {
                'question': quiz.question,
                'options': quiz.options,
                'start_date': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end_date': end_date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            all_quizzes.append(quiz_data)
        return JsonResponse({'quizzes': all_quizzes})
    except Quiz.DoesNotExist:
        return JsonResponse({'message': 'Quiz Empty'})
