from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import login as auth_login
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect(reverse('users:admin_hack'))
                return HttpResponseRedirect(reverse('xaki'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                authenticated_user = auth.authenticate(
                    username=user.email,
                    password=form.cleaned_data['password1']
                )
                if authenticated_user:
                    auth.login(request, authenticated_user)
                    return HttpResponseRedirect(reverse('xaki'))
                else:
                    return render(request, 'users/registration.html',
                        {'form': form, 'error': 'Ошибка при входе в аккаунт'})
            except IntegrityError:
                return render(request, 'users/registration.html',
                    {'form': form, 'error': 'Пользователь с такой почтой уже существует'})
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    context = {
        'user': request.user,
        'title': 'Profile'
    }
    return render(request, 'users/profile.html', context)

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Обработка полного имени
            full_name = form.cleaned_data.get('full_name')
            if full_name:
                name_parts = full_name.split()
                if len(name_parts) >= 2:
                    user.first_name = name_parts[0]
                    user.last_name = ' '.join(name_parts[1:])
            
            # Обработка остальных полей
            user.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.phone_number = form.cleaned_data.get('phone_number', '')
            user.gender = form.cleaned_data.get('gender', '')
            user.technology_stack = form.cleaned_data.get('technology_stack', '')
            user.group = form.cleaned_data.get('group', '')
            user.course = form.cleaned_data.get('course')
            user.student_number = form.cleaned_data.get('student_number', '')
            
            # Обработка фото
            if 'profile_photo' in request.FILES:
                user.profile_photo = request.FILES['profile_photo']
            
            user.save()
            return redirect('users:profile')
    else:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'date_of_birth': request.user.date_of_birth,
            'phone_number': request.user.phone_number,
            'gender': request.user.gender,
            'technology_stack': request.user.technology_stack,
            'group': request.user.group,
            'course': request.user.course,
            'student_number': request.user.student_number,
        }
        form = UserProfileForm(instance=request.user, initial=initial_data)
    
    return render(request, 'users/editprofile.html', {'form': form})

def changelogin(request):
    context = {'title': 'Profile'}
    return render(request, 'users/changelogin.html', context)

def addmail(request):
    context = {'title': 'Profile'}
    return render(request, 'users/addmail.html', context)

def addmailcorrect(request):
    context = {'title': 'Profile'}
    return render(request, 'users/addmailcorrect.html', context)

def restorepassword(request):
    context = {'title': 'Profile'}
    return render(request, 'users/restorepassword.html', context)

@login_required
def admin_hack(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('users:login'))
    context = {'title': 'Admin Panel'}
    return render(request, 'users/adminHack.html', context)

@login_required
def admin_list(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('users:login'))
    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    context = {
        'title': 'User List',
        'users': users
    }
    return render(request, 'users/adminList.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@login_required
@require_http_methods(["GET", "PUT"])
def user_detail(request, user_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        if request.method == "GET":
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(data)
            
        elif request.method == "PUT":
            data = json.loads(request.body)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.is_active = data.get('is_active', user.is_active)
            user.save()
            
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            })
            
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        data = json.loads(request.body)
        
        user.is_active = data.get('is_active', not user.is_active)
        user.save()
        
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

