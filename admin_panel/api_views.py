from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Blog
from .serializers import BlogSerializer

class BlogViewSet(viewsets.ModelViewSet):
  
    serializer_class = BlogSerializer
    queryset = Blog.objects.all().order_by("-created_at")

    def get_queryset(self):
        qs = super().get_queryset()

        search_query = (self.request.query_params.get("search") or "").strip()
        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(author_name__icontains=search_query) |
                Q(slug__icontains=search_query) |
                Q(status__icontains=search_query)
            )

        status_filter = (self.request.query_params.get("status") or "").strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs

    def perform_create(self, serializer):
        hashtags_value = (self.request.data.get("hashtags") or "").strip()
        serializer.save(
            hashtags=hashtags_value,
            tags=hashtags_value or serializer.validated_data.get("tags", "")
        )

    def perform_update(self, serializer):
        hashtags_value = (self.request.data.get("hashtags") or "").strip()
        serializer.save(
            hashtags=hashtags_value,
            tags=hashtags_value or serializer.validated_data.get("tags", "")
        )

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            "published_count": qs.filter(status="published").count(),
            "draft_count": qs.filter(status="draft").count(),
           
            "total": qs.count(),
        })