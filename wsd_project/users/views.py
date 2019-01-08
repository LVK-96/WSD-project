from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from .forms import SignupForm

class SignUp(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

def profilepage(request):
    username = request.user.username
    user = CustomUser.objects.get(username=username)
    return render(request, 'users/profile.html', {"user":user})