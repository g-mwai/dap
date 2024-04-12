from django.urls import  path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView

urlpatterns = [ 
    path("", views.landing, name="landing"),
    # path('404/', TemplateView.as_view(template_name='secondary/404.html'), name='404'),

    path("home/", views.home, name="home"),
    # path("home/view_post", views.view_post, name="view_post"),
    path("upload_post/", views.upload_post, name="upload_post"),
    path("upload_project/", views.upload_project, name="upload_project"),

    path("upload_gig/", views.upload_gig, name="upload_gig"),
    path("upload_sell/", views.upload_sell, name="upload_sell"),
    path("report/", views.report_post, name="report_post"),
    path("report_gig/", views.report_gig, name="report_gig"),
    path("report_bug/", views.report_bug, name="report_bug"),

    path("report_comment/", views.report_comment, name="report_comment"),
    
    path('posts/<int:post_id>/bookmark_status/', views.get_bookmark_status, name='bookmark_status'),
    path('posts/<int:comment_id>/comment_bookmark_status/', views.get_comment_bookmark_status, name='comment_bookmark_status'),

    path("p/<str:identifier>", views.post_detail, name="post_detail"),
    path("chats/", views.chat_list, name="chat_list"),
    path("manifesto/", views.manifesto, name="manifesto"),
    path('check_unread_alerts/', views.check_unread_alerts, name='check_unread_alerts'),
    path('mark_alerts_as_read/', views.mark_alerts_as_read, name='mark_alerts_as_read'),
    # path("home/baraza", views.baraza, name="baraza"),
    path("explore/", views.explore, name="explore"),
    path("members_list/", views.members_list, name="members_list"),
    path("booking/", views.booking, name="booking"),

    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('comment/<int:comment_id>/upvote/', views.upvote_comment, name='upvote_comment'),
    path('reply/<int:reply_id>/upvote/', views.upvote_reply, name='upvote_reply'),

    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),
    path('comment/<int:comment_id>/downvote/', views.downvote_comment, name='downvote_comment'),
    path('reply/<int:reply_id>/downvote/', views.downvote_reply, name='downvote_reply'),

    path('posts/<int:post_id>/get_comment_count/', views.get_comment_count, name='get_comment_count'),
    path('comments/<int:comment_id>/get_reply_count/', views.get_reply_count, name='get_reply_count'),

    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('upload_cover/', views.upload_cover, name='upload_cover'),

    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_avatar/', views.delete_avatar, name='delete_avatar'),
    path('delete_cover/', views.delete_cover, name='delete_cover'),

    # url(r'^ajax/uploads/$', views.upl.oadData, name='uploadData'),
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add-comment'),
    path('comments/<int:comment_id>/add_reply/', views.add_reply, name='add-reply'),

    # path("", views.store, name="store"),
    path("@<str:profile_username>", views.view_profile, name="view_profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # path('edit_profile_dyna/', views.edit_profile_dyna, name='edit_profile_dyna'),
    path('user_count_chart/', views.user_count_chart, name='user_count_chart'),

    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    # path('confirm_password/', views.confirm_password, name='confirm_password'),
    # path('confirm_username/', views.confirm_username, name='confirm_username'),
   
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_username/', views.edit_username, name='edit_username'),

    path('follow/<str:profile_username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:profile_username>/', views.unfollow_user, name='unfollow_user'),
    path('follow_user/', views.follow_user, name='follow_user'),
    # path("follow/@<str:profile_username>/",views.follow_toggle, name="follow_toggle"),
    path("@<str:profile_username>/following", views.follow_list, name="follow_list"),
    # path("like/<int:post_id>/",views.like_toggle, name="like_toggle"),
    path("search/", views.post_search, name="search_results"),
    # path('private-chat/<int:other_user_id>/', views.private_chat_view, name='private_chat'),
    path('alerts/', views.view_alerts, name='view_alerts'),
    path('market/', views.market, name='market'),
    path('fofo/', views.fofo, name='fofo'),
    path('toggle_pin/<int:post_id>/', views.toggle_pin, name='toggle_pin'),

    # path("free_store/", views.free_store, name="free_store"),
    # path("notification_list/", views.notification_list, name="notification_list"),
    path("settings/", views.settings, name="settings"),
    path("industries/", views.industry_list, name="industry_list"),

    path("bookmark_list/", views.bookmark_list, name="bookmark_list"),
    path('posts/<int:post_id>/toggle_bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('posts/<int:comment_id>/toggle_comment_bookmark/', views.toggle_comment_bookmark, name='toggle_comment_bookmark'),

    # path("profile/", views.profile, name="profile"),
    path('posts/<int:post_id>/toggle_repost/', views.toggle_repost, name='toggle_repost'),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("delete_reply/<int:reply_id>/", views.delete_reply, name="delete_reply"),
    path("delete_gig/<int:gig_id>/", views.delete_gig, name="delete_gig"),

    # topic filter
    path('i/<str:industry>/', views.industry_filter, name='industry_filter'),
    path('pol/<str:policy>/', views.policy, name='policy'),

    # xp filters
    path('xp/entry level/', views.xp_filter, {'experience': 'entry level'}, name='xp_entry level'),
    path('xp/senior level/', views.xp_filter, {'experience': 'senior level'}, name='xp_senior level'),
    path('xp/mid level/', views.xp_filter, {'experience': 'mid level'}, name='xp_mid level'),
    path('xp/no experience/', views.xp_filter, {'experience': 'no experience'}, name='xp_no experience'),

    # type filters
    path('type/part-time/', views.type_filter, {'gig_type': 'part-time'}, name='type_part-time'),
    path('type/full-time/', views.type_filter, {'gig_type': 'full-time'}, name='type_full-time'),
    path('type/contract/', views.type_filter, {'gig_type': 'contract'}, name='type_contract'),
    path('type/temporary/', views.type_filter, {'gig_type': 'temporary'}, name='type_temporary'),
    path('type/internship/', views.type_filter, {'gig_type': 'internship'}, name='type_internship'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)