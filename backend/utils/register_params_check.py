# -*- coding: utf-8 -*-
import re


def register_params_check(content: dict):
    # # 定义允许的字段及其对应的检查规则
    # required_fields = ["username", "password", "nickname", "mobile", "url"]
    # for field in required_fields:
    #     if field not in content:
    #         return field, False  # 如果缺少必填字段，返回字段名

    # 校验用户名
    username = content["username"]
    if (
        "username" not in content
        or not isinstance(username, str)
        or not re.match(r"^[a-zA-Z]+[0-9_-]+$", username)
        or not (5 <= len(username) <= 12)
    ):
        return "username", False

    # 校验密码
    password = content["password"]
    if (
        "password" not in content
        or not isinstance(password, str)
        or not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[-_*^])[A-Za-z\d\-_*^]{8,15}$", password
        )
    ):
        return "password", False

    # 校验昵称
    nickname = content["nickname"]
    if "nickname" not in content or not isinstance(nickname, str):
        return "nickname", False

    # 校验手机号
    mobile = content["mobile"]
    if (
        "mobile" not in content
        or not isinstance(mobile, str)
        or not re.match(r"^\+\d{2}\.\d{12}$", mobile)
    ):
        return "mobile", False

    # 校验url
    url = content.get("url")  # 先用 get 避免 KeyError
    if (
        "url" not in content
        or not isinstance(url, str)
        or not re.match(
            r"^(http://|https://)"
            r"[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
            r"(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
            r"(\.[a-zA-Z]{2,})$",
            url,
        )
    ):
        return "url", False

    # 校验 magic_number 是否为非负整数（如果传入了这个字段）
    magic_number = content.get("magic_number", 0)
    if not isinstance(magic_number, int) or magic_number < 0:
        return "magic_number", False

    # 返回 "ok" 和 True，表示所有校验通过
    content["magic_number"] = magic_number  # 设置默认值为 0
    return "ok", True
