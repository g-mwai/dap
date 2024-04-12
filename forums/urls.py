from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    # path("product_detail/<int:id>/", views.product_detail, name="product_detail"),
    # path("user_detail", views.user_detail, name="user_detail"),

  
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)