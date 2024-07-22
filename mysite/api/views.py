from rest_framework import generics

from .serializers import PostSerializer
from blog.models import Post


class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
