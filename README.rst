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

This is not a drop-in replacement for the wagtail image tag. Rather, you will need use
the normal easy_thumbnail tag in combination with a filter and a processor to work nicely
with wagtail images.


Quick start
-----------
1. Install ``wagtail_easy_thumbnails`` from Pypi::

    pip install wagtail_easy_thumbnails

2. Add ``wagtail_easy_thumbnails`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = (
        ...
        'wagtail_easy_thumbnails',
    )


3. Add the following filters to to your ``EASYTHUMBNAIL_PROCESSORS`` setting like this::

    THUMBNAIL_PROCESSORS = (
        # use this one instead of normal scale_and_crop
        'wagtail_easy_thumbnails.processors.wagtail_scale_and_crop_with_focal_area',
        # 'easy_thumbnails.processors.scale_and_crop',
        ... other processors
    )

4. Use in templates as follows::

    {% load thumbnail wagtail_thumbnail %}
    <img src="{% thumbnail page.visual|wagtail_thumbnailer 300x100 crop zoom=100 %}" alt=""/>

    <!--or-->

    {% thumbnail page.visual|wagtail_thumbnailer 300x100 crop zoom=100 as cropped_image %}
    <img src="{{ cropped_image.url }}"
         width="{{ cropped_image.width }}"
         height="{{ cropped_image.height }}"
         alt=""/>


5. Use in code as follows::

    from easy_thumbnails.files import get_thumbnailer

    ...

    properties = {
        'size': ...,
        'crop': True,
        'zoom': 100,
    }
    # image is the wagtail image (or subclass) instance
    wrapped_image = WagtailThumbnailerImageFieldFile(wagtail_image=image)

    # thumbnailer has the same properties as the template tag result, so .url, .width, etc.
    thumnailer = get_thumbnailer(wrapped_image).get_thumbnail(properties)



Thumbnail options
-----------------

The following options can be used to create the thumbnails. Also see the `Easy Thumbnails documentation`__ for all thumbnailing options.

__ http://easy-thumbnails.readthedocs.io/en/latest/index.html


``size`` is a required option, and defines the bounds that the generated image
must fit within. If one of either width or height is 0, the ratio of the original
image is used to determine the resulting width or height, respectively.

Other options are only provided if the given functionality is required:

- ``crop`` required to make the processor do anything. If not given, the normal ``scale_and_crop`` processor is used. Options for crop are not supported for this processor.
- ``zoom=<N>`` where N is an integer between 0 and 100 specifying how close to the focal area the image is cropped. Default is 0, meaning as close to the outer image boundaries as possible, 100 means as close to the focal area as possible.
- ``upscale`` if given and the resulting image is smaller that the requested size, the image is upscaled.

If the wagtail image does not have a focal area defined, the normal ``scale_and_crop`` processor
is used to generate the thumbnail.


Settings
--------
The following settings can be set to override the defaults. Also see the `Easy Thumbnails documentation`__
for all thumbnail settings.

__ http://easy-thumbnails.readthedocs.io/en/latest/ref/settings/

- ``WAGTAIL_FOCAL_AREA_IMAGE_DEBUG``: Defaults to ``False``. If set to ``True``, the focal area is drawn on the resulting image (useful for debugging).
- ``WAGTAIL_THUMBNAIL_ALWAYS_RECREATE`` Defaults to ``False``. If set to ``True``, the thumbnails are always regenerated, regardless of cached versions (useful for debugging)


License
-------
This software is released under the MIT License, see LICENSE.
