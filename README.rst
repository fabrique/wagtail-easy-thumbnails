=======================
Wagtail Easy Thumbnails
=======================

A simple django app that allows you to use  `easy_thumbnails`__ with the images from `Wagtail`__,
including the focal point that you can define on images in Wagtail.

__ https://github.com/SmileyChris/easy-thumbnails
__ https://wagtail.io/

This will allow you to use easy_thumbnail's features that the thumbnailer in Wagtail
does not provide, such as JPEG quality control per image, forcing images to JPEG and
the powerful extension mechanism of custom processors.

This is not a drop-in replacement for the wagtail image tag. Rather, you will use
the normal easy_thumbnail tag in combination with a filter and a processor to work nicely with wagtail images.

Quick start
-----------

1. Add ``wagtail_easy_thumbnails`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = (
        ...
        'wagtail_easy_thumbnails',
    )


2. Add the following filters to to your ``EASYTHUMBNAIL_PROCESSORS`` setting like this::

    THUMBNAIL_PROCESSORS = (
        # use this one instead of normal scale_and_crop
        'wagtail_easy_thumbnails.processors.wagtail_scale_and_crop_with_focal_area',
        # 'easy_thumbnails.processors.scale_and_crop',
        ... other processors
    )

3. Use in templates as follows::

    {% load thumbnail wagtail_thumbnail %}
    <img src="{% thumbnail page.visual|wagtail_thumbnailer 300x100 %}" alt=""/>


Thumbnail options
-----------------

The following options can be used to create the thumbnails.

``size`` is a required option, and defines the bounds that the generated image
must fit within. If one of either width or height is 0, the ratio of the original
image is used to determine the resulting width or height, respectively.

Other options are only provided if the given functionality is required:

- ``crop`` required to make the processor do anything. If not given, the normal
    ``scale_and_crop`` processor is used. Options for crop are not supported for this processor.
- ``zoom=<N>`` where N is an integer between 0 and 100 specifying how close
    to the focal area the image is cropped. Default is 0, meaning as close to the outer image
    boundaries as possible, 100 means as close to the focal area as possible.
- ``upscale`` if given and the resulting image is smaller that the requested size,
    the image is upscaled.

If the wagtail image does not have a focal area defined, the normal ``scale_and_crop`` processor
is used to generate the thumbnail.

Settings
--------
The following settings can be set to override the defaults

- ``WAGTAIL_FOCAL_AREA_IMAGE_DEBUG``: Defaults to ``False``. If set to ``True``, the
    focal area is drawn on the resulting image (useful for debugging).
- ``WAGTAIL_THUMBNAIL_ALWAYS_RECREATE`` Defaults to ``False``. If set to ``True``, the
    thumbnails are always regenerated, regardless of cached versions (useful for debugging)
