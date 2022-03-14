from django.shortcuts import render
from django.db.models import Q,Count
from django.core.paginator import Paginator ,EmptyPage , PageNotAnInteger
from blog.models import Post
from courses.models import Course


def home(request):
    latest_courses = Course.objects.get_publish_course()[:8]
    popular_courses = Course.objects.get_popular_course()[:8]
    posts = Post.objects.annotate(count=Count('visits')).order_by('-count')[:8]
    context = {'latest_courses':latest_courses , 'popular_courses':popular_courses , 'posts':posts}
    return render(request,'index.html',context)

def contact_us(request):
    return render(request , 'contact.html')

def search(request):
    searched = request.GET.get('search-word')
    print(request.GET.get('page'))
    if request.GET.get('page'):
        searched = request.session.get('search')
    else:
        request.session['search'] = searched

    searched_courses = Course.objects.filter(Q(title__icontains=searched) | Q(description__icontains=searched) | Q(tags__name__icontains=searched) |
                                    Q(categories__title__icontains=searched)).distinct()

    count = searched_courses.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(searched_courses, 3)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request , 'archive.html' , {'searched':searched, 'courses' : courses , 'count': count , 'paginator':paginator})
