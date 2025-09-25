from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from post import controllers
from utils.jwt import login_required
from utils.post_params_check import post_params_check
from utils.reply_post_params_check import reply_post_params_check


class PostListView(APIView):
    """
    处理帖子列表的视图类
    """

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "description": "页码"},
                    "size": {"type": "integer", "description": "每页数量"},
                    "userId": {"type": "integer", "description": "用户ID"},
                    "orderByReply": {
                        "type": "boolean",
                        "description": "是否按回复数排序",
                    },
                },
                "required": [],
            }
        },
        responses={
            200: OpenApiResponse(
                description="获取帖子列表成功",
                response={
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "description": "页码"},
                        "size": {"type": "integer", "description": "每页数量"},
                        "total": {"type": "integer", "description": "总数"},
                        "posts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "description": "帖子ID"},
                                    "userId": {
                                        "type": "integer",
                                        "description": "用户ID",
                                    },
                                    "nickname": {
                                        "type": "string",
                                        "description": "用户昵称",
                                    },
                                    "title": {
                                        "type": "string",
                                        "description": "帖子标题",
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "帖子内容",
                                    },
                                    "lastRepliedUserId": {
                                        "type": "integer",
                                        "description": "最新回复用户id，默认为发帖人",
                                    },
                                    "lastRepliedNickname": {
                                        "type": "string",
                                        "description": "最新回复用户昵称，默认为发帖人",
                                    },
                                    "lastRepliedTime": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "最新回复时间",
                                    },
                                    "created": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "帖子创建时间",
                                    },
                                    "updated": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "帖子更新时间",
                                    },
                                },
                            },
                        },
                    },
                },
            ),
            500: OpenApiResponse(description="服务器内部错误"),
        },
        description="获取帖子列表",
        summary="获取帖子列表",
        operation_id="get_post_list",
    )
    @login_required
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 10))
        user_id = request.GET.get("userId", 0)
        order_by_reply = bool(request.GET.get("orderByReply", False))

        post_list, count, result = controllers.get_post_list(user_id, page, size, order_by_reply)
        if result:
            return Response(
                {
                    "posts": post_list,
                    "page": page,
                    "size": size,
                    "total": count,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"message": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "帖子标题"},
                    "content": {"type": "string", "description": "帖子内容"},
                },
                "required": ["title", "content"],
            }
        },
        responses={
            200: OpenApiResponse(
                description="创建帖子成功",
                response={
                    "type": "object",
                    "properties": {
                        "postId": {"type": "integer", "description": "帖子ID"},
                        "message": {"type": "string", "description": "消息"},
                    },
                },
            ),
            400: OpenApiResponse(description="请求参数错误"),
            500: OpenApiResponse(description="服务器内部错误"),
        },
        description="发布帖子",
        summary="发布帖子",
    )
    @login_required
    def post(self, request, *args, **kwargs):
        try:
            content = request.data
            if not content:
                return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)

            key, passed = post_params_check(content)
            if not passed:
                return Response(
                    {"message": "invalid arguments: " + key},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            post_id, result = controllers.create_post(
                content["title"], content["content"], request.user.id
            )

            if result:
                return Response({"postId": post_id, "message": "ok"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """
    获取帖子详情与回帖列表的视图
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="postId",
                type=int,
                location=OpenApiParameter.PATH,
                description="帖子的id",
            ),
        ],
        request=None,
        responses={
            200: OpenApiResponse(
                description="获取帖子详情成功",
                response={
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "帖子ID"},
                        "userId": {"type": "integer", "description": "用户ID"},
                        "nickname": {"type": "string", "description": "用户昵称"},
                        "title": {"type": "string", "description": "帖子标题"},
                        "content": {"type": "string", "description": "帖子内容"},
                        "created": {
                            "type": "string",
                            "format": "date-time",
                            "description": "帖子创建时间",
                        },
                        "updated": {
                            "type": "string",
                            "format": "date-time",
                            "description": "帖子更新时间",
                        },
                        "reply": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "description": "回帖ID"},
                                    "userId": {
                                        "type": "integer",
                                        "description": "用户ID",
                                    },
                                    "nickname": {
                                        "type": "string",
                                        "description": "用户昵称",
                                    },
                                    "postId": {
                                        "type": "integer",
                                        "description": "帖子ID",
                                    },
                                    "replyId": {
                                        "type": "integer",
                                        "description": "回复目标回复Id，不提供表示回复主楼",
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "回帖内容",
                                    },
                                    "created": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "回帖创建时间",
                                    },
                                    "updated": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "回帖更新时间",
                                    },
                                },
                            },
                            "description": "回帖列表，创建时间升序",
                        },
                    },
                },
            ),
            404: OpenApiResponse(description="未找到帖子"),
            500: OpenApiResponse(description="服务器内部错误"),
        },
        description="获取帖子详情",
        summary="获取帖子详情",
        operation_id="get_post_detail",
    )
    @login_required
    def get(self, request, postId, *args, **kwargs):
        detail, result = controllers.get_post_detail(postId)
        if result:
            return Response(detail, status=status.HTTP_200_OK)
        else:
            return Response({"message": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="postId",
                type=int,
                location=OpenApiParameter.PATH,
                description="帖子的id，需要是本人所发帖才能修改",
            ),
        ],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "帖子标题"},
                    "content": {"type": "string", "description": "帖子内容"},
                },
                "required": ["title", "content"],
            }
        },
        responses={
            200: OpenApiResponse(
                description="更新帖子成功",
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "操作结果信息"},
                    },
                },
            ),
            400: OpenApiResponse(description="请求参数错误"),
            404: OpenApiResponse(description="未找到帖子"),
            500: OpenApiResponse(description="服务器内部错误"),
        },
        description="编辑当前用户发布的帖子",
        summary="更新帖子",
    )
    @login_required
    def put(self, request, postId, *args, **kwargs):
        try:
            content = request.data
            if not content:
                return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)

            key, passed = post_params_check(content)
            if not passed:
                return Response(
                    {"message": "invalid arguments: " + key},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            check = controllers.check_post(postId, request.user.id)
            if not check:
                return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)

            result = controllers.update_post(
                content["title"], content["content"], postId, request.user.id
            )

            if result:
                return Response({"message": "ok"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="postId",
            type=int,
            location=OpenApiParameter.PATH,
            description="回复帖子的id",
        ),
    ],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "回帖内容"},
                "replyId": {
                    "type": "integer",
                    "description": "回复目标回复Id，不提供表示回复主楼",
                },
            },
            "required": ["content"],
        }
    },
    responses={
        200: OpenApiResponse(description="回复帖子成功"),
        400: OpenApiResponse(description="请求参数错误"),
        404: OpenApiResponse(description="未找到回复"),
        500: OpenApiResponse(description="服务器内部错误"),
    },
    description="回复帖子",
    summary="回复帖子",
)
@api_view(["POST"])
@login_required
def reply_post(request, postId):
    try:
        content = request.data
        if not content:
            return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)

        key, passed = reply_post_params_check(content)
        if not passed:
            return Response(
                {"message": "invalid arguments: " + key},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "replyId" in content:
            reply_id = content["replyId"]
            check = controllers.check_reply(postId, reply_id)
            if not check:
                return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            reply_id = 0

        result = controllers.create_reply(content["content"], request.user.id, postId, reply_id)

        if result:
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except KeyError:
        return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="postId",
            type=int,
            location=OpenApiParameter.PATH,
            description="回复帖子的id",
        ),
        OpenApiParameter(
            name="replyId",
            type=int,
            location=OpenApiParameter.PATH,
            description="修改回复的id",
        ),
    ],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "修改回帖的内容"},
            },
            "required": ["content"],
        }
    },
    responses={
        200: OpenApiResponse(description="修改回复成功"),
        400: OpenApiResponse(description="请求参数错误"),
        404: OpenApiResponse(description="未找到回复"),
        500: OpenApiResponse(description="服务器内部错误"),
    },
    description="修改回复",
    summary="编辑当前用户发布的回帖",
)
@api_view(["PUT"])
@login_required
def modify_reply(request, postId, replyId):
    try:
        content = request.data
        if not content:
            return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)

        key, passed = reply_post_params_check(content)
        if not passed:
            return Response(
                {"message": "invalid arguments: " + key},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check = controllers.check_self_reply(replyId, request.user.id)
        if not check:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)

        result = controllers.update_reply(content["content"], request.user.id, postId, replyId)

        if result:
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except KeyError:
        return Response({"message": "bad arguments"}, status=status.HTTP_400_BAD_REQUEST)
