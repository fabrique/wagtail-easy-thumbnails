from django.template import Library

from wagtail_easy_thumbnails.utils import WagtailThumbnailerImageFieldFile

register = Library()


@register.filter
def wagtail_thumbnailer(obj):
    """
    Convert a wagtail image to a thumbnailer instance.

    The reference to the original wagtail image is kept as wagtail_image property
    :param obj: a wagtail image
    :return: a thumbnailer instance, with reference to original wagtail image
    """
    return WagtailThumbnailerImageFieldFile(obj)
