from .models import Category

def all_categories(request):
    categories = Category.objects.all()
    return {'all_categories':categories}