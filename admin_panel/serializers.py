from rest_framework import serializers
from .models import Blog,Lead

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