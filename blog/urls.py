from django.urls import  path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("", views.blog, name="blog"),
    path("article_detail/", views.article_detail, name="article_detail"),
    path("article_topic/", views.article_topic, name="article_topic"),
    path("article_tag/", views.article_tag, name="article_tag"),

    #  # topics filter
    # path('topics/motorsports/', views.topic_filter, {'topic': 'motorsports'}, name='topic_motorsports'),
    # path('topics/project/', views.topic_filter, {'topic': 'project'}, name='topic_project'),
    # path('topics/culture/', views.topic_filter, {'topic': 'culture'}, name='topic_culture'),
    # path('topics/mods/', views.topic_filter, {'topic': 'modifications'}, name='topic_modifications'),
    # path('topics/news/', views.topic_filter, {'topic': 'news'}, name='topic_news'),
    # path('topics/humour/', views.topic_filter, {'topic': 'humour'}, name='topic_humour'),
    # path('topics/stories/', views.topic_filter, {'topic': 'stories'}, name='topic_stories'),
    # path('topics/events/', views.topic_filter, {'topic': 'events'}, name='topic_events'),
    # path('topics/questions/', views.topic_filter, {'topic': 'questions'}, name='topic_questions'),
    # path('topics/tips/', views.topic_filter, {'topic': 'tips & tricks'}, name='topic_tips & tricks'),
    # path("dashboard/", views.dashboard, name="dashboard"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)