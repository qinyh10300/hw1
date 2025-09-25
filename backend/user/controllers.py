from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import User


def get_user(user_id):
    try:
        u = User.objects.get(id=user_id)
        return u, True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False


def create_user(username, password, nickname, url, mobile, magic_number):
    try:
        now = timezone.now()
        u = User.objects.create(
            username=username,
            password=password,
            nickname=nickname,
            url=url,
            mobile=mobile,
            magic_number=magic_number,
            created=now,
            updated=now,
        )
        u.save()
        return True
    except Exception as e:
        print(e)
        return False


def get_user_with_pass(username, password):
    try:
        u = User.objects.get(username=username)
        if not u.password == password:
            return "not found", False
        return u, True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False
