import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker
from questions.models import Tag, Question, Answer, QuestionLike, AnswerLike
from core.models import Profile

fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Наполнить базу тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент наполнения')

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f'Начинаем наполнение с ratio={ratio}...')

        # 1. Пользователи и профили
        users = []
        profiles = []
        for i in range(ratio):
            username = f'user_{i+1}'
            email = f'{username}@example.com'
            user = User(username=username, email=email)
            users.append(user)
            profiles.append(Profile(user=user, nickname=fake.user_name()))
        User.objects.bulk_create(users)
        created_users = User.objects.filter(username__startswith='user_')[:ratio]
        for i, user in enumerate(created_users):
            profiles[i].user = user
        Profile.objects.bulk_create(profiles)
        self.stdout.write(f'Создано {ratio} пользователей')

        # 2. Теги
        tags = []
        for i in range(ratio):
            tags.append(Tag(name=f'tag_{i+1}'))
        Tag.objects.bulk_create(tags)
        created_tags = Tag.objects.filter(name__startswith='tag_')[:ratio]
        self.stdout.write(f'Создано {ratio} тегов')

        # 3. Вопросы
        questions = []
        user_list = list(created_users)
        for i in range(ratio * 10):
            q = Question(
                title=fake.sentence(nb_words=6),
                text=fake.text(max_nb_chars=500),
                author=random.choice(user_list),
                likes_count=random.randint(0, 1000)
            )
            questions.append(q)
        Question.objects.bulk_create(questions)
        created_questions = Question.objects.all()[:ratio*10]
        # Привязываем теги
        through_model = Question.tags.through
        through_objects = []
        for question in created_questions:
            num_tags = random.randint(1, 3)
            chosen_tags = random.sample(list(created_tags), num_tags)
            for tag in chosen_tags:
                through_objects.append(
                    through_model(question_id=question.id, tag_id=tag.id)
                )
        through_model.objects.bulk_create(through_objects)
        self.stdout.write(f'Создано {ratio*10} вопросов')

        # 4. Ответы
        answers = []
        question_list = list(created_questions)
        for i in range(ratio * 100):
            a = Answer(
                question=random.choice(question_list),
                author=random.choice(user_list),
                text=fake.text(max_nb_chars=300),
                is_correct=random.random() < 0.05,
                likes_count=random.randint(0, 500)
            )
            answers.append(a)
        Answer.objects.bulk_create(answers)
        created_answers = Answer.objects.all()[:ratio*100]
        self.stdout.write(f'Создано {ratio*100} ответов')

        # 5. Лайки вопросов
        q_likes = []
        max_q_likes = min(ratio * 200, ratio * 10 * ratio)
        # Заранее собираем существующие пары в set
        existing_q_likes = set(
            QuestionLike.objects.values_list('user_id', 'question_id')
        )
        i = 0
        while i < max_q_likes:
            user = random.choice(user_list)
            question = random.choice(question_list)
            if (user.id, question.id) not in existing_q_likes:
                q_likes.append(QuestionLike(user=user, question=question))
                existing_q_likes.add((user.id, question.id))  # обновляем set
                i += 1
        QuestionLike.objects.bulk_create(q_likes, ignore_conflicts=True)
        self.stdout.write(f'Создано лайков вопросов: {len(q_likes)}')

        # 6. Лайки ответов
        a_likes = []
        answer_list = list(created_answers)
        max_a_likes = min(ratio * 200, ratio * 100 * ratio)
        existing_a_likes = set(
            AnswerLike.objects.values_list('user_id', 'answer_id')
        )
        i = 0
        while i < max_a_likes:
            user = random.choice(user_list)
            answer = random.choice(answer_list)
            if (user.id, answer.id) not in existing_a_likes:
                a_likes.append(AnswerLike(user=user, answer=answer))
                existing_a_likes.add((user.id, answer.id))
                i += 1
        AnswerLike.objects.bulk_create(a_likes, ignore_conflicts=True)
        self.stdout.write(f'Создано лайков ответов: {len(a_likes)}')

        self.stdout.write(self.style.SUCCESS(
            f'Наполнение завершено!'
        ))
