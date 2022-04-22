from django.shortcuts import render
from .models import Course , Comment
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.contrib import messages
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from .forms import CaptchaForm


def course_list(request):
    all_courses = Course.objects.all()
    count = all_courses.count()
    page = request.GET.get('page', 1)

    paginator = Paginator(all_courses, 6)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request , 'archive.html' , {'courses' : courses , 'count': count , 'paginator':paginator})

def course_detail(request,slug):
    course = get_object_or_404(Course,slug=slug)
    if request.user.ip_address not in course.visits.all():
        course.visits.add(request.user.ip_address)
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        body = request.POST.get('body')
        if form.is_valid():
            user_comment = Comment.objects.create(course=course,user=request.user)
            user_comment.body = body
            user_comment.save()
            messages.success(request , 'کامنت شما با موفقیت افزوده شد.')
    else:
        form = CaptchaForm()

    page = request.GET.get('page')
    all_comments = course.comment.get_active_comments()

    paginator = Paginator(all_comments, 3)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)


    return render(request,'single.html' , {'course':course , 'form':form , 'comments' : comments , 'paginator':paginator })

def category_courses(request,slug):
    category_name = str(slug).replace('-',' ')
    all_courses = Course.objects.get_course_by_category(category_name)
    count = all_courses.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_courses, 3)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request , 'archive.html' , {'searched':category_name, 'courses' : courses , 'count': count , 'paginator':paginator})

def tag_courses(request,slug):
    tag = get_object_or_404(Tag, slug=slug)
    all_courses = Course.objects.filter(tags__name__in=[tag])
    count = all_courses.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_courses, 3)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request , 'archive.html' , {'searched':tag, 'courses' : courses , 'count': count , 'paginator':paginator})

def course_filter(request):
    all_courses = Course.objects.get_publish_course()
    sorted_courses= None
    filtered_courses = None
    kind = request.GET.get('kind')
    sort = request.GET.get('order')

    if request.GET.get('page'):
        kind = request.session.get('kind')
        sort = request.session.get('sort')
    else:
        request.session['kind'] = kind
        request.session['sort'] = sort

    if kind == 'free':
        filtered_courses = all_courses.filter(price=0)
    elif kind == 'notfree':
        filtered_courses = all_courses.filter(price__gt=0)
    else:
        filtered_courses = all_courses

    if sort == 'price':
        sorted_courses = filtered_courses.order_by('price')
    elif sort == 'length':
        sorted_courses = sorted(filtered_courses,key=lambda c:c.get_sec(),reverse=True)
    else:
        sorted_courses = filtered_courses.order_by('-created')

    count = sorted_courses.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(sorted_courses, 3)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request , 'archive.html' , {'courses' : courses , 'count': count , 'paginator':paginator})
