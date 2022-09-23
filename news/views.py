from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, \
    get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import News, Comment, NewsStatus, CommentStatus, LikeDislikeNews, Status, LikeDislikeComment
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer
from account.models import Author
from .permissions import IsAuthorPermission, IsAdminPermission


class NewsListCreateAPIview(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsAuthorPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def get_queryset(self):
        return self.queryset.all()


class NewsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return self.queryset.filter(news_id=self.kwargs['news_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news=get_object_or_404(News, id=self.kwargs['news_id'])
        )


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]


class StatusViewSet(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class StatusRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAdminPermission, ]


class PostNewsLike(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, news_id, status_slug):
        news = get_object_or_404(News, id=news_id)
        news_status = get_object_or_404(Status, slug=status_slug)
        try:
            like_dislike = NewsStatus.objects.create(news=news, author=request.user.author, status=news_status)
        except IntegrityError:
            like_dislike = NewsStatus.objects.get(news=news, author=request.user.author)
            if like_dislike.status == news_status:
                like_dislike.status = None
            else:
                like_dislike.status = news_status
            like_dislike.save()
            data = {"error": "You already added status"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": "Status added"}
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentLike(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, news_id, comment_id, status_slug):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_status = get_object_or_404(Status, slug=status_slug)
        try:
            like_dislike = CommentStatus.objects.create(comment=comment, author=request.user.author, status=comment_status)
        except IntegrityError:
            like_dislike = CommentStatus.objects.get(comment=comment, author=request.user.autho)
            like_dislike.status = comment_status
            like_dislike.save()
            data = {"error": "You already added status"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": "Status added"}
            return Response(data, status=status.HTTP_201_CREATED)
