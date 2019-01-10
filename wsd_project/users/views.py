from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import SignupForm, ChangeForm, ProfileUpdateForm

def signup(request):
    form = SignupForm
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profilepage(request):
    u_form = ChangeForm
    p_form = ProfileUpdateForm
    username = request.user.username
    user = CustomUser.objects.get(username=username)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html', {"user":user})

    
