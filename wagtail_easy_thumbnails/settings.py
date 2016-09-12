# -*- coding: utf-8 -*-
from django.conf import settings

WAGTAIL_FOCAL_AREA_IMAGE_DEBUG = getattr(settings, 'WAGTAIL_FOCAL_AREA_IMAGE_DEBUG', False)

WAGTAIL_THUMBNAIL_ALWAYS_RECREATE = getattr(settings, 'WAGTAIL_THUMBNAIL_ALWAYS_RECREATE', False)
