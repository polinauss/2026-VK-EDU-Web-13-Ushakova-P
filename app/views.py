from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects, request, per_page=5):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def fake_questions():
    return [
        {
            "id": i,
            "title": f"How to build a moon park {i}?",
            "text": "Guys, I have trouble with a moon park...",
            "likes": 5
        } for i in range(1, 21)
    ]


def index(request):
    page = paginate(fake_questions(), request)
    return render(request, "index.html", {"page": page})


def hot(request):
    page = paginate(fake_questions(), request)
    return render(request, "hot.html", {"page": page})


def tag(request, name):
    page = paginate(fake_questions(), request)
    return render(request, "tag.html", {"page": page, "tag": name})


def question(request, id):
    answers = [{"text": f"Answer {i}", "likes": i} for i in range(1, 10)]
    page = paginate(answers, request)
    return render(request, "question.html", {"page": page})


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def profile(request):
    return render(request, "profile.html")
