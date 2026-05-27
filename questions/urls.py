from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [\
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('question/<int:pk>/', views.question_detail, name='question'),
    path('question/<int:pk>/like/', views.question_like, name='question_like'),
    path('answer/<int:pk>/like/', views.answer_like, name='answer_like'),
    path('answer/<int:pk>/correct/', views.answer_correct, name='answer_correct'),
    path('ask/', views.ask, name='ask'),
]
