from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Blog,Lead, Property
from .serializers import BlogSerializer, LeadSerializer, PropertySerializer


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

class LeadViewSet(viewsets.ModelViewSet):
   
    serializer_class = LeadSerializer
    queryset = Lead.objects.all().order_by("-created_at")

    def get_queryset(self):
        qs = super().get_queryset()

        enquiry_type = (self.request.query_params.get("type") or "").strip()
        source_filter = (self.request.query_params.get("source") or "").strip()
        new_leads = (self.request.query_params.get("new") or "").strip().lower()
        search_query = (self.request.query_params.get("search") or "").strip()

        if enquiry_type:
            qs = qs.filter(enquiry_type=enquiry_type)

        if source_filter:
            qs = qs.filter(source=source_filter)

        if new_leads == "true":
            qs = qs.filter(source="Enquire Now")

        if search_query:
            qs = qs.filter(
                Q(full_name__icontains=search_query) |
                Q(mobile_number__icontains=search_query) |
                Q(place__icontains=search_query) |
                Q(remarks__icontains=search_query)
            )

        return qs

    @action(detail=False, methods=["get"])
    def summary(self, request):
        # Same counts you calculated in the HTML view
        return Response({
            "general_count": Lead.objects.filter(enquiry_type="General").count(),
            "international_count": Lead.objects.filter(enquiry_type="International").count(),
            "domestic_count": Lead.objects.filter(enquiry_type="Domestic").count(),
            "new_leads_count": Lead.objects.filter(source="Enquire Now").count(),
            "total": Lead.objects.count(),
        })


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by("-created_at")
    serializer_class = PropertySerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()

        # optional filters
        ptype = (self.request.query_params.get("property_type") or "").strip()
        location = (self.request.query_params.get("location") or "").strip()
        search = (self.request.query_params.get("search") or "").strip()

        if ptype:
            qs = qs.filter(property_type=ptype)

        if location:
            qs = qs.filter(location__icontains=location)

        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(location__icontains=search)
                | Q(address__icontains=search)
                | Q(summary__icontains=search)
                | Q(owner_name__icontains=search)
                | Q(owner_contact__icontains=search)
                | Q(amenities__icontains=search)
            )

        return qs