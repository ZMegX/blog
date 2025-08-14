from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Added import here
from django.contrib import messages #import for messages

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm 
from .models import Profile

# Create your views here.
def dashboard(request):
    return render(request, "users/dashboard.html")

def register(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()  # get the created User instance
      Profile.objects.get_or_create(user=user)
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created for {username}!')
      return redirect('login')
  else:
    form = CustomUserCreationForm()
  return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, 
                request.FILES, 
                instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Your account has been updated') #Changes here
      return redirect('profile') #Changes here
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'u_form': u_form,
    'p_form': p_form
  }

  return render(request, 'users/profile.html', context)