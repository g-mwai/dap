from django.urls import path
from . import views 
# from .views import BookmarkToggleAPI
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')


urlpatterns = [
    # path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("new_poll/", views.new_poll, name="new_poll"),
    path("new_yesno/", views.new_yesno, name="new_yesno"),
    path("new_sell/", views.new_sell, name="new_sell"),
    path("new_gig/", views.new_gig, name="new_gig"),

    path('api/', include(router.urls)),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)