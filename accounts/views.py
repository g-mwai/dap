from django.shortcuts import  render, redirect
from .forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import AuthenticationForm 
from core.views  import  home, edit_profile
from .models import *
from django.contrib.auth.decorators import login_required
from .utils import generate_random_code, send_password_reset_email
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.backends import ModelBackend  # Import the authentication backend


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create or update UserCount
            today = timezone.now().date()
            user_count, _ = UserCount.objects.get_or_create(date=today)
            user_count.count += 1
            user_count.save()
            user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(edit_profile)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    context = {
        "register_form": form,
        
    }
    return render(request, "auth/register.html", context)


def login_request(request):
	if request.method == "POST":
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Welcome, you are now logged in as {username}.")
				return redirect("profile")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = LoginForm()
	return render(request=request, template_name="auth/login.html", context={"login_form":form})


# @login_required
# def my_profile(request):
    
#     profile = Profile.objects.filter(user=request.user)
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile) 

#         if form.is_valid() and profile_form.is_valid():
#             form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated successfully')
#             return redirect(request.META['HTTP_REFERER'])
#     else:
#         form = EditProfileForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
    
#     profiles = Profile.objects.all()
#     context ={
#         'profiles': profiles,
#         'form': form,
#         'profile_form': profile_form
       
#     }
#     return render (request, 'users/profile.html', context )

def logout_request(request):
	logout(request)
	return redirect("/")

def password_reset_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        password_change_request = get_object_or_404(PasswordChangeRequest, code=code)

        if password_change_request.is_expired():
            messages.error(request, 'Password reset link has expired.')
            return redirect('request_password_reset')

        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent logout
            password_change_request.delete()  # Remove the password change request after successful update
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')  # Redirect to login or another page

    else:
        form = SetPasswordForm(request.user)

    return render(request, 'settings/password_reset_confirm.html', {'form': form})


def request_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            # Generate a random code
            code = generate_random_code()

            # Create a PasswordChangeRequest
            password_change_request = PasswordChangeRequest.objects.create(user=user, code=code)

            # Send email with code and link
            send_password_reset_email(user, code)

            messages.success(request, 'Password reset code sent to your email. Check your inbox.')
            return redirect('password_reset_confirm')

    return render(request, 'settings/request_password_reset.html')


def fofo(request):
	context ={

       
    }
	return render (request, '404.html', context )