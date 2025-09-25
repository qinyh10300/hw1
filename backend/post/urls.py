from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/post", views.PostListView.as_view(), name="post_list"),
    path("api/v1/post/<int:postId>", views.PostDetailView.as_view(), name="post_detail"),
    path("api/v1/post/<int:postId>/reply", views.reply_post, name="reply_post"),
    path("api/v1/post/<int:postId>/reply/<int:replyId>", views.modify_reply, name="modify_reply"),
]
