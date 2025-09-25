import datetime

from django.db.models import F

from .models import Post, Reply


def get_post_list(user_id=0, page=1, size=10, order_by_reply=False):
    try:
        if order_by_reply:
            order_col = "last_replied_time"
        else:
            order_col = "updated"

        if user_id == 0:
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(user_id=user_id)

        post_list = (
            posts.annotate(
                nickname=F("user__nickname"),
                lastRepliedNickname=F("last_replied_user__nickname"),
            )
            .order_by("-" + order_col)[(page - 1) * size : page * size]
            .values(
                "id",
                "nickname",
                "title",
                "content",
                "lastRepliedNickname",
                "created",
                "updated",
                userId=F("user_id"),
                lastRepliedUserId=F("last_replied_user_id"),
                lastRepliedTime=F("last_replied_time"),
            )
        )
        count = posts.count()

        return list(post_list), count, True
    except Exception as e:
        print(e)
        return [], 0, False


def check_post(post_id, user_id):
    try:
        p = Post.objects.filter(id=post_id).first()
        if p.user_id == int(user_id):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def check_reply(post_id, reply_id):
    try:
        if reply_id == 0:
            p = Post.objects.filter(id=post_id).first()
            if p is None:
                return False
            else:
                return True
        else:
            r = Reply.objects.filter(id=reply_id).first()
            if r.post_id == int(post_id):
                return True
            else:
                return False
    except Exception as e:
        print(e)
        return False


def check_self_reply(reply_id, user_id):
    try:
        r = Reply.objects.filter(id=reply_id).first()
        if r.user_id == int(user_id):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def create_post(title, content, user_id):
    try:
        now = datetime.datetime.now()
        p = Post.objects.create(
            user_id=user_id,
            title=title,
            content=content,
            last_replied_user_id=user_id,
            last_replied_time=now,
            created=now,
            updated=now,
        )
        return p.id, True
    except Exception as e:
        print(e)
        return 0, False


def update_post(title, content, post_id, user_id):
    try:
        now = datetime.datetime.now()
        Post.objects.filter(id=post_id, user_id=user_id).update(
            title=title, content=content, updated=now
        )
        return True
    except Exception as e:
        print(e)
        return False


def get_post_detail(post_id):
    try:
        post = (
            Post.objects.filter(id=post_id)
            .values(
                "id",
                "title",
                "content",
                "created",
                "updated",
                userId=F("user_id"),
                nickname=F("user__nickname"),
                lastRepliedTime=F("last_replied_time"),
            )
            .first()
        )

        reply_list = (
            Reply.objects.filter(post_id=post_id)
            .values(
                "id",
                "content",
                "created",
                "updated",
                nickname=F("user__nickname"),
                userId=F("user_id"),
                postId=F("post_id"),
                replyId=F("reply_id"),
            )
            .order_by("created")
        )

        reply_list = list(reply_list)

        for reply in reply_list:
            reply["replyId"] = reply["replyId"] if reply["replyId"] else 0

        post["reply"] = reply_list
        return post, True
    except Exception as e:
        print(e)
        return None, False


def create_reply(content, user_id, post_id, reply_id=0):
    try:
        now = datetime.datetime.now()
        reply = Reply.objects.create(
            user_id=user_id,
            post_id=post_id,
            content=content,
            created=now,
            updated=now,
        )
        if reply_id:
            reply.reply_id = reply_id
            reply.save()
        Post.objects.filter(id=post_id).update(last_replied_time=now, last_replied_user_id=user_id)
        return True
    except Exception as e:
        print(e)
        return False


def update_reply(content, user_id, post_id, reply_id):
    try:
        now = datetime.datetime.now()
        Reply.objects.filter(id=reply_id, user_id=user_id).update(content=content, updated=now)
        Post.objects.filter(id=post_id).update(last_replied_time=now, last_replied_user_id=user_id)
        return True
    except Exception as e:
        print(e)
        return False
