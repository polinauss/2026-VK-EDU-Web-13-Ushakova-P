from django.shortcuts import render, redirect
from django.urls import reverse
from .utils import paginate
import re

QUESTIONS = [
    {'id': 1,  'title': 'Как правильно настроить виртуальное окружение в Python?', 'text': 'Каждый раз при создании проекта venv ломается...', 'answers_count': 12, 'likes': 8,  'tags': ['python', 'venv']},
    {'id': 2,  'title': 'Почему Django не видит мои static файлы?', 'text': 'collectstatic отрабатывает, но в браузере 404...', 'answers_count': 7,  'likes': 15, 'tags': ['django', 'static']},
    {'id': 3,  'title': 'Как сделать миграции после изменения модели?', 'text': 'makemigrations ничего не создаёт...', 'answers_count': 5,  'likes': 4,  'tags': ['django', 'migrations']},
    {'id': 4,  'title': 'Лучший способ подключить MySQL к Django?', 'text': 'Пробую mysqlclient, но ошибка при migrate...', 'answers_count': 9,  'likes': 11, 'tags': ['mysql', 'django']},
    {'id': 5,  'title': 'Как настроить GitHub Actions для Django проекта?', 'text': 'CI/CD не запускается...', 'answers_count': 3,  'likes': 6,  'tags': ['git', 'django']},
    {'id': 6,  'title': 'Почему запросы к БД такие медленные?', 'text': 'EXPLAIN показывает Full Table Scan...', 'answers_count': 4,  'likes': 9,  'tags': ['mysql', 'optimization']},
    {'id': 7,  'title': 'Как сделать кастомную User модель в Django?', 'text': 'Хочу email вместо username...', 'answers_count': 8,  'likes': 14, 'tags': ['django', 'auth']},
    {'id': 8,  'title': 'Docker + Django + PostgreSQL — как поднять?', 'text': 'Не могу подключиться из контейнера...', 'answers_count': 11, 'likes': 18, 'tags': ['docker', 'django']},
]

def index(request):
    page = paginate(QUESTIONS, request, per_page=5)
    return render(request, 'questions/index.html', {'page_obj': page})

def hot(request):
    # Сортируем по лайкам для горячих вопросов
    hot_questions = sorted(QUESTIONS, key=lambda x: x['likes'], reverse=True)
    page = paginate(hot_questions, request, per_page=5)
    return render(request, 'questions/hot.html', {'page_obj': page})

def tag(request, tag):
    filtered = [q for q in QUESTIONS if tag.lower() in [t.lower() for t in q['tags']]]
    page = paginate(filtered or QUESTIONS, request, per_page=5)
    return render(request, 'questions/tag.html', {'page_obj': page, 'tag': tag})

def question_detail(request, pk):
    question = next((q for q in QUESTIONS if q['id'] == pk), None)
    if not question and QUESTIONS:
        question = QUESTIONS[0]
    
    answers = [
        {'text': 'Попробуй python manage.py collectstatic --noinput', 'likes': 7, 'is_correct': True, 'author': 'DjangoExpert', 'created_at': '2 hours ago'},
        {'text': 'Убедись что STATICFILES_DIRS правильно указан', 'likes': 3, 'is_correct': False, 'author': 'WebDev', 'created_at': '5 hours ago'},
        {'text': 'Проверь настройки в settings.py: STATIC_URL и STATIC_ROOT', 'likes': 5, 'is_correct': False, 'author': 'PythonGuru', 'created_at': '1 day ago'},
    ]
    
    # Пагинация для ответов (передаём page_obj, но шаблон пока использует answers)
    page = paginate(answers, request, per_page=3)
    
    return render(request, 'questions/question.html', {
        'question': question, 
        'answers': answers,
        'page_obj': page
    })

def ask(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        text = request.POST.get('text', '').strip()
        tags = request.POST.get('tags', '').strip()
        
        # Валидация
        errors = {}
        
        if not title:
            errors['title'] = 'Title is required'
        elif len(title) > 200:
            errors['title'] = 'Title must be less than 200 characters'
            
        if not text:
            errors['text'] = 'Question text is required'
        elif len(text) < 10:
            errors['text'] = 'Please provide more details (at least 10 characters)'
            
        if tags:
            tag_list = [t.strip().lower() for t in tags.split(',') if t.strip()]
            if len(tag_list) > 5:
                errors['tags'] = 'Maximum 5 tags allowed'
            for tag in tag_list:
                if not re.match(r'^[a-z0-9-]+$', tag):
                    errors['tags'] = 'Tags can only contain lowercase letters, numbers, and hyphens'
                    break
        
        if errors:
            return render(request, 'questions/ask.html', {
                'form_errors': errors,
                'error': 'Please fix the errors below'
            })
        
        # Здесь в будущем будет сохранение в БД
        return render(request, 'questions/ask.html', {
            'success': f'Question "{title}" has been posted successfully!',
        })
    
    return render(request, 'questions/ask.html')
