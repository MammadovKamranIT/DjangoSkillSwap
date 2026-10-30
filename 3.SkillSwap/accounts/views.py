from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import LoginForm, RegisterForm

from django.contrib.auth import authenticate, get_user_model, login, logout

# Create your views here.
def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=identifier, password=password)
            if user is None:
                User = get_user_model()
                try:
                    candidate = User.objects.get(username=identifier, password=password)
                except User.DoesNotExist:
                    candidate = None
                if candidate is not None:
                    user = authenticate(request, username=candidate.username, password=password)
            if user is not None:
                login(request, user)
                request.session["active_user"] = user.get_username()
                messages.success(request, "You are now logged in.")
                return redirect('accounts:dashboard')
            form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
  
    return render(request, 'accounts/login.html',  {'form': form})



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user= User.objects.create_user(
                username= form.cleaned_data["username"],
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"]
             
            )

            login(request, user)
            messages.success(request, "Thank you for registering")
            return redirect("accounts:dashboard")
    else:
        form = RegisterForm()
    return render (request, 'accounts/register.html', {"form": form})



def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'active_user': request.session.get('active_user','Guest')}, )


@login_required
def logout_view(request):
    if request.method != "POST":
        return render(request, "accounts/logout_confirm.html")
    logout(request)
    request.session["active_user"] = None
    messages.info(request, "You are now logged out.")
    return redirect('home')


def register_success_view(request):
    return redirect(request, 'accounts:dashboard', {'active_user': request.session.get('active_user','Guest')},)