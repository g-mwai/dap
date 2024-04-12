from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import *

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login", kwargs={"authentication_form":LoginForm}),
    # path("profile", views.my_profile, name="profile"),
    path("fofo", views.fofo, name="fofo"),
    path("logout", views.logout_request, name= "logout"),
    path('password_reset/', views.request_password_reset, name='request_password_reset'),
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)