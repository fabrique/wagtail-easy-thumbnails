from __future__ import absolute_import

from easy_thumbnails.files import ThumbnailerFieldFile
from .settings import WAGTAIL_THUMBNAIL_ALWAYS_RECREATE


class WagtailThumbnailerImageFieldFile(ThumbnailerFieldFile):
    """
    Extension of normal ThumbnailerFieldFile that adds optional focal area based on wagtail image.
    """

    def __init__(self, wagtail_image, *args, **kwargs):
        """
        Keep track of the wagtail image to use the focal area.
        :param wagtail_image: a Wagtail image
        """
        self.wagtail_image = wagtail_image
        file = wagtail_image.file
        super(WagtailThumbnailerImageFieldFile, self).__init__(file.instance, file.field, file.name, *args, **kwargs)

    def get_options(self, thumbnail_options, **kwargs):
        """
        Adds the wagtail image cropping information as implicit options if not already set.
        :return: the options for the processors
        """
        opts = super(WagtailThumbnailerImageFieldFile, self).get_options(thumbnail_options, **kwargs)
        if 'focal_area' not in opts and self.wagtail_image.has_focal_point():
            opts['focal_area'] = (
                self.wagtail_image.focal_point_x,
                self.wagtail_image.focal_point_y,
                self.wagtail_image.focal_point_width,
                self.wagtail_image.focal_point_height,
            )
        return opts

    def thumbnail_exists(self, *args, **kwargs):
        """
        Allow a shortcut with setting to always recreate thumbnails.
        Useful for debugging.
        """
        if WAGTAIL_THUMBNAIL_ALWAYS_RECREATE:
            return False
        return super(WagtailThumbnailerImageFieldFile, self).thumbnail_exists(*args, **kwargs)
