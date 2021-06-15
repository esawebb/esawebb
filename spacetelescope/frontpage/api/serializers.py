from rest_framework import serializers

from djangoplicity.archives.utils import get_instance_archives_urls
from djangoplicity.media.d2d.serializers import ImageSerializer
from djangoplicity.media.models import Image
from djangoplicity.utils.templatetags.djangoplicity_text_utils import remove_html_tags


class ESASkyImageSerializer(ImageSerializer):
    """

    """


class ESASkySerializer(serializers.ModelSerializer):
    """
    Custom Image serializer for the ESASky JSONFeed
    """

    assets = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()
    # description = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'title', 'reference_url', 'credit', 'assets')

    def get_assets(self, obj):
        return {
            "Resources": get_instance_archives_urls(obj)
        }

    def get_credit(self, obj):
        return remove_html_tags(obj.credit)

    def get_description(self, obj):
        return remove_html_tags(obj.description)
