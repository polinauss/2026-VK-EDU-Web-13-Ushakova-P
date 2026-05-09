from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from .models import Question, Answer, Tag, QuestionLike, AnswerLike
from .forms import QuestionForm, AnswerForm
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
    tag_obj = get_object_or_404(Tag, name=tag)
    questions = Question.objects.by_tag(tag).prefetch_related('tags')
    page = paginate(questions, request, per_page=5)
    return render(request, 'questions/tag.html', {'page_obj': page, 'tag': tag})

def question_detail(request, pk):
    question = get_object_or_404(Question.objects.prefetch_related('tags', 'answers'), pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect(f'{reverse("questions:question", args=[pk])}?page=1#answer-{answer.id}')
    else:
        form = AnswerForm()
    answers = question.answers.all().order_by('-created_at')
    page = paginate(answers, request, per_page=3)
    return render(request, 'questions/question.html', {
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
        'form': form,
    })

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_tags(question)
            return redirect('questions:question', pk=question.id)
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})


@login_required
def question_like(request, pk):
    question = get_object_or_404(Question, pk=pk)
    liked = QuestionLike.objects.filter(user=request.user, question=question).exists()
    if liked:
        QuestionLike.objects.filter(user=request.user, question=question).delete()
        question.likes_count -= 1
    else:
        QuestionLike.objects.create(user=request.user, question=question)
        question.likes_count += 1
    question.save()
    return JsonResponse({'likes_count': question.likes_count, 'liked': not liked})

@login_required
def answer_like(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    liked = AnswerLike.objects.filter(user=request.user, answer=answer).exists()
    if liked:
        AnswerLike.objects.filter(user=request.user, answer=answer).delete()
        answer.likes_count -= 1
    else:
        AnswerLike.objects.create(user=request.user, answer=answer)
        answer.likes_count += 1
    answer.save()
    return JsonResponse({'likes_count': answer.likes_count, 'liked': not liked})
