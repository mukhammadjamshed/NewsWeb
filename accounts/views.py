from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views import View



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('You are now logged in.')
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    profile_info = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile_info
    }

    return render(request, 'pages/user_profile.html', context)


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
        else:
            error_message = 'There was an error with your form submission. Please try again.'
            context = {
                'user_form': user_form,
                'error_message': error_message,
            }
            return render(request, 'account/register.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'account/register.html', context)

@login_required
def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')


    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile_edit.html', {"user_form": user_form, "profile_form": profile_form})



class UserEditView(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)


        return render(request, 'account/profile_edit.html', {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        if request.method == 'POST':
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)


        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('user_profile')

