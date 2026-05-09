from django.shortcuts import render, get_object_or_404
from .models import Question
from .utils import paginate

def index(request):
    questions = Question.objects.new().prefetch_related('tags')
    page = paginate(questions, request, per_page=5)
    return render(request, 'questions/index.html', {'page_obj': page})

def hot(request):
    questions = Question.objects.popular().prefetch_related('tags')
    page = paginate(questions, request, per_page=5)
    return render(request, 'questions/hot.html', {'page_obj': page})

def tag(request, tag):
    questions = Question.objects.by_tag(tag).prefetch_related('tags')
    page = paginate(questions, request, per_page=5)
    return render(request, 'questions/tag.html', {'page_obj': page, 'tag': tag})

def question_detail(request, pk):
    question = get_object_or_404(Question.objects.prefetch_related('tags', 'answers'), pk=pk)
    answers = question.answers.all().order_by('-created_at')
    page = paginate(answers, request, per_page=3)
    return render(request, 'questions/question.html', {
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
    })

def ask(request):
    # заглушка, без изменений
    return render(request, 'questions/ask.html')
