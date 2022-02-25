from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import  Paginator , PageNotAnInteger ,EmptyPage
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course
from .forms import QuestionForm
from .models import Question , Answer

def questions(request , slug=None):
    if slug:
        all_questions = Question.objects.filter(active=True , course__slug=slug).order_by('-created')
        latest_questions = Question.objects.all().order_by('-created')[:6]
    else:
        all_questions = Question.objects.filter(active=True).order_by('-created')
        latest_questions = all_questions[:6]

    courses= Course.objects.get_publish_course()
    page_number = request.GET.get('page')
    paginator = Paginator(all_questions, 4)
    try:
        questions = paginator.get_page(page_number)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    context = {'questions' : questions , 'latest_questions' : latest_questions, 'courses' : courses , 'paginator':paginator }

    return render(request , 'questions/question_list.html' , context)

def question(request , slug):
    question = get_object_or_404(Question , slug=slug)
    if request.method == 'POST':
        body = request.POST.get('answer')
        if request.body:
            answer = Answer.objects.create(body=body,user=request.user,question=question)
            answer.save()
            messages.success(request , 'پاسخ شما با موفقیت ارسال شد')
        else:
            messages.error(request , 'خطایی رخ داد')

    return render(request, 'questions/question_detail.html' , {'question':question })

@login_required(login_url='/questions/')
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.slug = slugify(form.cleaned_data['title'])
            question.save()
            messages.success(request , 'سوال شما اضافه شد')
            return redirect('question_list')
    else:
        form = QuestionForm()

    return render(request ,'questions/ask_question.html', {'form':form})
