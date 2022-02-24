from .models import PostCategory

def blog_categories(request):
    return {'blog_categories' : PostCategory.objects.all()}