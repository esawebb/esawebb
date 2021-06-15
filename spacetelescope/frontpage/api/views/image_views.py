from rest_framework import generics, renderers

from djangoplicity.media.models import Image
from djangoplicity.media.options import ImageOptions

from spacetelescope.frontpage.api.serializers import ESASkyImageSerializer, ESASkySerializer

from spacetelescope.frontpage.api.paginators import ESASkyPaginator


class ESASkyListView(generics.ListAPIView):
    """

    """

    serializer_class = ESASkySerializer
    pagination_class = ESASkyPaginator
    renderer_classes = (renderers.JSONRenderer, )

    def get_queryset(self):
        qs = ImageOptions.Queries.zoomable.queryset(Image, ImageOptions, self.request)[0].order_by('-release_date')
        return qs
