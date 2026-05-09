from .models import Tag

def popular_tags(request):
    tags = Tag.objects.order_by('?')[:10]
    return {'popular_tags': tags}
