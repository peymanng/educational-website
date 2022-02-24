from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, PageNotAnInteger , EmptyPage
from taggit.models import Tag
from .models import Post , PostCategory


def posts(request, tag_slug=None):
    all_posts = Post.objects.all().order_by('-pub_date')
    categories = PostCategory.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_posts = Post.objects.filter(tags__name__in=[tag])
    page_number = request.GET.get('page')
    paginator = Paginator(all_posts, 4)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'tag': tag , 'paginator':paginator}

    return render(request, 'blog/post_list.html', context)

def post(request,slug):
    post = get_object_or_404(Post , slug=slug)
    return render(request , 'blog/post_detail.html' , {"post" : post})

def posts_by_category(request,slug):
    category_name = str(slug).replace('-',' ')
    all_posts = get_list_or_404(Post , category__slug=slug)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 4)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    return render(request , 'blog/post_list.html' , {'posts' : courses ,'paginator':paginator})