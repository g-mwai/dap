from django.contrib.auth.decorators import user_passes_test

def superuser_required(function):
    """
    Decorator for views that checks if the user is a superuser.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/login/',  # Optional: Redirect URL if user is not a superuser
        redirect_field_name=None  # Optional: Specify the query string parameter name for the redirect URL
    )
    return actual_decorator(function)
