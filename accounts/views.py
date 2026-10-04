from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import LoginForm, UserRegistrationForm, UserEditForm , ProfileEditForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username = data['username'],password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Muvaffaqiyatli login amalga oshirildi!')
                else:
                    return HttpResponse('Profil faol emas')
            else:
                HttpResponse('Login yoki parolda hatolik bor!')
    else:
        form = LoginForm()

    return render(request,'registration/login.html', {'form':form})

def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    context = {
        'user': user,
        'profile':profile,
    }

    return render(request, 'pages/user_profile.html', context)

def user_register(request):
    if request.method == 'POST':

        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user':new_user
            }
            return render(request,'account/register_done.html',context)
    else:
        user_form = UserRegistrationForm()

    return render(request,'account/register.html', {'user_form':user_form})


class UserSignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login_page_view')
    template_name = 'account/register.html'


class SignupView(View):
    def get(self,request):
        user_form = UserRegistrationForm

        return render(request, 'account/register.html', { 'user_form': user_form})

    def post(self,request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()

            return render(request, 'account/register_done.html', { 'user_form': user_form})
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,'account/profile_edit.html',{'user_form':user_form,'profile_form':profile_form})

class EditProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self,request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
