from django.db import models


# Create your models here.
class Post(models.Model):
    """
    帖子
    """

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="发帖用户")

    title = models.CharField(max_length=255, verbose_name="帖子标题")
    content = models.CharField(max_length=255, verbose_name="帖子内容")

    last_replied_user = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="last_replied_posts",
        verbose_name="最新回复的用户",
    )
    last_replied_time = models.DateTimeField(null=True, verbose_name="最新回复时间")

    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")


class Reply(models.Model):
    """
    回复
    """

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="回复用户")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="回复帖子")
    reply = models.ForeignKey(
        "post.Reply",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="回复帖子",
        default=None,
    )

    content = models.CharField(max_length=255, verbose_name="帖子内容")

    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
