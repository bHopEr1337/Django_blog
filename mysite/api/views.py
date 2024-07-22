from django.forms import model_to_dict
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer
from blog.models import Post, User, Test_products_for_rest


# class PostAPIView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class PostAPIView(APIView):
    def get(self, request):
        """Обработчик GET запросов"""
        posts = Test_products_for_rest.objects.all().values()
        return Response({'posts': posts})

    def post(self, request):
        """Обработчик POST запросов"""
        post = Test_products_for_rest.objects.create(
            title=request.data['title'],
            body=request.data['body'],
        )
        return Response(model_to_dict(post), status=status.HTTP_201_CREATED)
