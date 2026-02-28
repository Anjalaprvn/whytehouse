from rest_framework import serializers
from .models import Blog,Lead, Property

class BlogSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "status",
            "package_id",
            "author_name",
            "author_summary",
            "reading_time",
            "publish_date",
            "featured_image",
            "featured_image_url",
            "hashtags",
            "tags",
            "created_at",
            "updated_at",
            "image_url",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "image_url"]

    def get_image_url(self, obj):
        return obj.image_url

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            "id",
            "full_name",
            "mobile_number",
            "place",
            "source",
            "enquiry_type",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]



class PropertySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    amenity_list = serializers.ReadOnlyField()

    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "property_type",
            "location",
            "website",
            "address",
            "summary",
            "owner_name",
            "owner_contact",
            "amenities",
            "amenity_list",   # ✅ split list for frontend
            "image",
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None