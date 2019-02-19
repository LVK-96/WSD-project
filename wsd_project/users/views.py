from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from store.models import Highscore
from .models import CustomUser
from .forms import SignupForm, ChangeForm, ProfileUpdateForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.http import HttpResponse

user_login_required = user_passes_test(lambda user: user.is_active, login_url='/')
def active_user_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            user.is_active = False
            user.save() 
            current_site = get_current_site(request)
            subject = 'Activate your wsd18store account'
            message = render_to_string('users/confirm_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            send_mail(subject, message, 'wsd18@store.com', [user.email], fail_silently=False)
            
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')

@active_user_required
def profilepage(request):
    if Highscore.objects.filter(player_id=request.user.pk):
        myhighscores = Highscore.objects.filter(player_id=request.user.pk)
    else:
        myhighscores = None

    if request.method == 'POST':
        u_form = ChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profilepage')
    else:
        u_form = ChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'highscores': myhighscores
    }
    
    return render(request, 'users/profile.html', context)

    
