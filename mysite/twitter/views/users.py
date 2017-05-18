from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from services import notify, profile_nav
from twitter.models import Followship
from twitter.forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user = User.objects.create_user(
                request.POST.get('username'),
                request.POST.get('email'),
                request.POST.get('password'),
            )
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {
        'form': form,
    })

@login_required
def follow(request, username):
    login_user = request.user
    visited_user = get_object_or_404(User, username=username)
    if login_user != visited_user:
        if not profile_nav.check_followship(login_user, visited_user):
            follow = Followship(
                initiative_user = login_user,
                followed_user = visited_user,
            )
            follow.save()
            notify.notify_follow(login_user, visited_user)
    return redirect('profile', username=username)

@login_required
def unfollow(request, username):
    login_user = request.user
    visited_user = get_object_or_404(User, username=username)
    if login_user != visited_user:
        Followship.objects.filter(
                initiative_user=login_user,
                followed_user=visited_user,
            ).delete()
    return redirect('profile', username=username)