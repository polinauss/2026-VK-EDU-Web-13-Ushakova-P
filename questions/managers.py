from django.db import models

class QuestionManager(models.Manager):
    def new(self):
        return self.get_queryset().order_by('-created_at')

    def popular(self):
        return self.get_queryset().order_by('-likes_count')

    def by_tag(self, tag_name):
        return self.get_queryset().filter(tags__name=tag_name).order_by('-created_at')
