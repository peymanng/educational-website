from django.contrib.auth import authenticate , login , get_user_model , logout , update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import UpdateUserForm
from .models import Profile
from courses.models import Course

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return  redirect('/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')
        user = authenticate(request,username=username ,password=password)
        if user is not None:
            login(request , user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('profile')
        messages.error(request , 'نام کاربری یا رمز عبور نادرست است.')
        return render(request , 'login.html')
    return render(request , 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request,'این نام کاربری ثبت شده است.')
            return redirect('signup')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'ایمیل از قبل ثبت شده است.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username , email=email)
                user.set_password(password)
                user.save()
                return redirect('login')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(redirect_field_name='/')
def profile(request):
    return render(request, 'profile.html')

@login_required(redirect_field_name='/')
def update_user(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'حساب کاربری شما با موفقیت تغییر یافت.')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'user_changes.html', {'form': user_form})

@login_required(redirect_field_name='/')
def update_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت.')
            return redirect('/')
        else:
            messages.error(request, 'لطفا غلط های زیر را تصحیح کنید.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user_changes.html', {
        'form': form
    })

@login_required(redirect_field_name='/')
def update_prof_pic(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        prof = get_object_or_404(Profile, user=request.user)
        prof.image = image
        prof.save()
        return redirect('profile')

    return render(request , 'upload_image_form.html')

@login_required(redirect_field_name='/')
def user_courses(request):
    courses = request.user.student_courses.all()
    return render(request , 'user_courses.html' , {'courses':courses})