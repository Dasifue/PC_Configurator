from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, mixins
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from django.contrib.auth.forms import PasswordChangeForm

from .models import User
from .forms import RegisterForm, LoginForm, UserUpdateForm


class RegisterView(generic.FormView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("main:main")

    def post(self, request):
        form: RegisterForm = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            messages.success(request=request, message="Registered successfully")
            return redirect(self.success_url)
        return render(request=request, template_name=self.template_name, context={ "form":form })
    

class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = reverse_lazy("main:main")

    def post(self, request):
        form: LoginForm = self.form_class(data=request.POST)
        if form.is_valid():
            user = authenticate(request=request, username=form.cleaned_data.get("email"), password=form.cleaned_data.get("password"))
            if user is not None:
                login(request=request, user=user)
                messages.success(request=request, message="Logined successfully")
                return redirect(self.success_url)
            else:
                messages.error(request=request, message="Error: check email or password")
        return render(request=request, template_name=self.template_name, context={ "form":form })
    

class LogoutView(mixins.LoginRequiredMixin, View):
    success_url = reverse_lazy("account:login")

    def get(self, request):
        logout(request)
        return redirect(self.success_url)


class UserDetailsView(mixins.LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "profile.html"
    pk_url_kwarg = "pk"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["configurations"] = context["user"].configurations.all()
        return context
    

class UpdateProfileView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "update.html"

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request=request, template_name=self.template_name, context={ "form":form })
    
    def post(self, request):
        form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            print(request.POST, request.FILES, "\n\n\n")
            messages.success(request=request, message="Profile was updated successfully")
            return redirect(reverse("account:profile", kwargs={"pk":request.user.pk}))
        return render(request=request, template_name=self.template_name, context={ "form":form })
    

class ChangePasswordView(mixins.LoginRequiredMixin, generic.FormView):
    form_class = PasswordChangeForm
    template_name = "change_password.html"

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request=request, template_name=self.template_name, context={ "form":form })
    
    def post(self, request):
        form = self.form_class(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request=request, message="Password was changed successfully")
            return redirect(reverse("account:profile", kwargs={"pk":request.user.pk}))
        return render(request=request, template_name=self.template_name, context={ "form":form })