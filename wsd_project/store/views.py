from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from .forms import NewGameForm
from django.urls import reverse_lazy
#from django.contrib.auth.decorators import login_required
#from django.utils.decorators import method_decorator

from .models import Game

# Create your views here.
def index(request):
    return render(request, 'store/home.html')

def games(request):
    return render(request, 'store/games.html')

def highscores(request):
    return render(request, 'store/highscores.html')


#add a login required decorator
class AddGame(generic.CreateView):
    form_class = NewGameForm
    success_url = reverse_lazy('')#where does it redirect?
    template_name = 'store/addgame.html'
    #@method_decorator(login_required)
    def form_valid(self, form):
        #check that the user is dev
        #ran when a valid form is submitted
        form.instance.dev = self.request.user#set the developer of this game as the user
        return super().form_valid(form)
