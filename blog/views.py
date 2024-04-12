from django.shortcuts import render, redirect
from accounts.forms import *
from core.views import home
from django.contrib import messages
from django.contrib.auth import login, authenticate 

# Create your views here.


def blog(request):
    form = LoginForm(request, data=request.POST)
    signup_form = NewUserForm(request.POST)
    if request.method == "POST":
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect(edit_profile)
        messages.error(request, "Unsuccessful registration. Invalid information.")

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = LoginForm()
    signup_form = NewUserForm()
    context ={
        "login_form": form,
        "signup_form": signup_form,
    }

    return render (request, 'blog/index.html', context )

def article_detail(request):
    context = {

    }

    return render (request, 'blog/post_detail.html', context )

def article_topic(request):
    context = {

    }

    return render (request, 'blog/index.html', context )

def article_tag(request):
    context = {

    }

    return render (request, 'blog/index.html', context )
