from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from accounts.forms import LoginForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, "Incorrect login or password")
            return redirect('index')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.warning(request, "Username is not found")
            return redirect('index')
        login(request, user)
        if user:
            return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        context = {'form': form}
        return self.render_to_response(context)