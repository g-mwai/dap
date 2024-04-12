from django.urls import  path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("", views.dashboard, name="dashboard"),
    path("members/", views.members, name="members"),
    path('user_count_chart/', views.user_count_chart, name='user_count_chart'),
    path("posts/", views.posts, name="posts"),
    path("earnings/", views.earnings, name="earnings"),
    path("reports/", views.reports, name="reports"),
    path("reported_post/<int:id>", views.reported_post, name="reported_post"),
    path("reported_comment/<int:id>", views.reported_comment, name="reported_comment"),
    path("reported_gig/<int:id>", views.reported_gig, name="reported_gig"),
    path("reported_bug/<int:id>", views.reported_bug, name="reported_bug"),

    path('delete_reported_post/<int:post_id>/', views.delete_reported_post, name='delete_reported_post'),
    path('delete_reported_comment/<int:comment_id>/', views.delete_reported_comment, name='delete_reported_comment'),
    path('delete_reported_gig/<int:gig_id>/', views.delete_reported_gig, name='delete_reported_gig'),
    path('delete_reported_bug/<int:bug_id>/', views.delete_reported_bug, name='delete_reported_bug'),


    path('keep_reported_post/<int:post_id>/', views.keep_reported_post, name='keep_reported_post'),
    path('keep_reported_comment/<int:comment_id>/', views.keep_reported_comment, name='keep_reported_comment'),
    path('keep_reported_gig/<int:gig_id>/', views.keep_reported_gig, name='keep_reported_gig'),

    path("post_article/", views.post_article, name="post_article"),
    
    path("docs/", views.docs, name="docs"),
    path("new_doc/", views.new_doc, name="new_doc"),
    path("doc_detail/<int:id>", views.doc_detail, name="doc_detail"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)