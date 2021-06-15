import os

from django.core.files.storage import FileSystemStorage

from djangoplicity.archives.resources import ImageFileType, ResourceFile
from djangoplicity.media.consts import MEDIA_CONTENT_SERVERS


def get_tiles_for_instance(instance, fileclass=ResourceFile):
    """

    """

    resource_format = 'zoomable'
    localbase = os.path.join(instance.Archive.Meta.root, "{}{}{}".format(resource_format, os.sep, instance.id))
    file_extension = ImageFileType.exts[0]
    storage = FileSystemStorage()
    resource = None
    tiles = []

    if storage.exists(localbase):
        resource = fileclass(localbase, storage)

    if resource and hasattr(instance, 'content_server') and instance.content_server and instance.content_server_ready:
        try:
            content_server = MEDIA_CONTENT_SERVERS[instance.content_server]
        except KeyError:
            content_server = None

        if content_server:
            archive_class_name = "".format(instance.__module__, instance.__class__.__name__)
            try:
                archive_formats = content_server.formats[archive_class_name]
            except KeyError:
                # No content server defined for this format
                archive_formats = []

            if resource_format in archive_formats:
                tiles_location = os.path.join(
                    storage.location, "{}{}{}".format(instance.Archive.Meta.root, os.sep, resource_format)
                )
                base_url = os.path.join(content_server.get_url(resource, resource_format), instance.Archive.Meta.root)
                tile_groups = os.listdir(tiles_location)
                for tiles_dir in tile_groups:
                    if os.path.isdir(tiles_dir):
                        print(tiles_dir)

    return tiles
