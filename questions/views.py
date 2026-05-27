from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
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

# ------------------ Лайки/дизлайки ------------------
def _toggle_like(model_like, obj, user, like=True):
    """
    model_like: QuestionLike или AnswerLike
    obj: Question или Answer
    user: пользователь
    like: True - поставить лайк, False - дизлайк (в данной реализации дизлайк просто убирает лайк)
    """
    # Проверка, что тип действия валиден
    if like not in (True, False):
        return None

    liked = model_like.objects.filter(user=user, **{obj.__class__.__name__.lower(): obj}).exists()

    if like and not liked:
        # поставить лайк
        model_like.objects.create(user=user, **{obj.__class__.__name__.lower(): obj})
        obj.likes_count += 1
        obj.save()
        return {'likes_count': obj.likes_count, 'liked': True}
    elif not like and liked:
        # убрать лайк (дизлайк)
        model_like.objects.filter(user=user, **{obj.__class__.__name__.lower(): obj}).delete()
        obj.likes_count -= 1
        obj.save()
        return {'likes_count': obj.likes_count, 'liked': False}
    else:
        # уже в нужном состоянии
        return {'likes_count': obj.likes_count, 'liked': liked}

@require_POST
@login_required
def question_like(request, pk):
    question = get_object_or_404(Question, pk=pk)
    like = request.POST.get('like')  # '1' или '0'
    if like not in ('0', '1'):
        return JsonResponse({'error': 'Invalid like parameter'}, status=400)
    result = _toggle_like(QuestionLike, question, request.user, like == '1')
    if result is None:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    return JsonResponse(result)

@require_POST
@login_required
def answer_like(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    like = request.POST.get('like')  # '1' или '0'
    if like not in ('0', '1'):
        return JsonResponse({'error': 'Invalid like parameter'}, status=400)
    result = _toggle_like(AnswerLike, answer, request.user, like == '1')
    if result is None:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    return JsonResponse(result)

# ------------------ Отметка правильного ответа ------------------
@require_POST
@login_required
def answer_correct(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question = answer.question

    # Проверка, что пользователь — автор вопроса
    if request.user != question.author:
        return JsonResponse({'error': 'Только автор вопроса может отмечать правильный ответ.'}, status=403)

    # Сбрасываем предыдущий правильный ответ, если есть
    if answer.is_correct:
        answer.is_correct = False
        message = 'Правильный ответ снят.'
    else:
        # снимаем пометку с других ответов
        Answer.objects.filter(question=question, is_correct=True).update(is_correct=False)
        answer.is_correct = True
        message = 'Ответ отмечен как правильный.'

    answer.save()
    return JsonResponse({
        'is_correct': answer.is_correct,
        'answer_id': answer.id,
        'message': message
    })
