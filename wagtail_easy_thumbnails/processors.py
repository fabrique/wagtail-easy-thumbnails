from .settings import WAGTAIL_FOCAL_AREA_IMAGE_DEBUG

from easy_thumbnails import processors
try:
    from PIL import Image, ImageChops, ImageFilter, ImageDraw
except ImportError:
    import Image
    import ImageChops
    import ImageFilter
    import ImageDraw


def wagtail_scale_and_crop_with_focal_area(im, size, crop=False, focal_area=None, zoom=None, upscale=False, **kwargs):
    """
    Like ``easy_thumbnails.processors.scale_and_crop``, but will use the
    coordinates in ``focal_area`` to make sure that as much of the focal
    area is in the cropped image, with the center of the focal area as much
    as possible in the center of the cropped image.

    If no focal area is given, normal scale_and_crop is used.

    Please not that this does *not* work correctly if the image has been
    resized by a previous processor (e.g ``autocrop``).

    ``crop`` needs to be set to True for this to work
        (otherwise normal crop_and_scale is used)
    ``focal_area`` needs to be an x,y,width,height tuple
        (where x,y is the center of the focal area)

    ``zoom`` will determine how close to the focal area the crop is:
        100 is as close as possible to the focal area
        0 is close as possible to the edge of the image
        The zoom level is automatically adjusted when the target size
        is larger than the zoom size (regardless of ``upscale``)

    ``upscale`` if True, the resulting image (with possible adjusted ``zoom``) is
        blown up to match the requested size if it's not large enough.
    """
    if not (focal_area and crop):
        # use the normal scale_and_crop if either focal_area or crop is not defined
        return processors.scale_and_crop(im, size, zoom=zoom, crop=crop,
                                         upscale=upscale, **kwargs)

    if not zoom:
        zoom = 0

    # from here on we have a focal area and cropping is on
    source_x, source_y = [float(v) for v in im.size]
    target_x, target_y = [float(v) for v in size]

    # determine the scale (target_x or target_y can be 0)
    scale = max(target_x / source_x, target_y / source_y)

    # Handle one-dimensional targets.
    if not target_x:
        target_x = source_x * scale
    elif not target_y:
        target_y = source_y * scale

    focal_cx, focal_cy, focal_width, focal_height = focal_area

    target_ratio = target_x / target_y
    image_ratio = source_x / source_y
    focal_ratio = focal_width / focal_height

    # determine the width,height for the extreme zoom levels
    zoom_0_width = round(min(source_y * target_ratio, source_y * image_ratio))
    zoom_0_height = round(min(source_x / target_ratio, source_x / image_ratio))

    zoom_100_width = round(max(focal_height * target_ratio, focal_height * focal_ratio))
    zoom_100_height = round(max(focal_width / target_ratio, focal_width / focal_ratio))

    # make sure full zoom is never larger than no zoom
    if zoom_100_width > zoom_0_width or zoom_100_height > zoom_0_height:
        zoomed_width = zoom_0_width
        zoomed_height = zoom_0_height
        zoom_ratio = 0
    elif zoom_100_width < target_x or zoom_100_height < target_y:
        # max possible zoom should not be smaller than target size if possible
        zoomed_width = min(target_x, zoom_0_width)
        zoomed_height = min(target_y, zoom_0_height)
        # could also use zoom height, shouldn't matter
        zoom_ratio = 1 - (zoom_0_width - zoomed_width / (zoom_0_width - zoom_100_width))
    else:
        # determine zoomed_width and height for given zoom
        zoom_ratio = zoom / 100
        zoomed_width = -(zoom_ratio * (zoom_0_width - zoom_100_width) - zoom_0_width)
        zoomed_height = -(zoom_ratio * (zoom_0_height - zoom_100_height) - zoom_0_height)

    # determine scale to get from zoomed_width to target_width
    zoom_scale = target_x / zoomed_width

    if WAGTAIL_FOCAL_AREA_IMAGE_DEBUG:
        # draw focal area for debugging
        rect = Image.new('RGBA', im.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(rect)
        x0 = int(focal_cx - (focal_width / 2))
        y0 = int(focal_cy - (focal_height / 2))
        x1 = int(focal_cx + (focal_width / 2))
        y1 = int(focal_cy + (focal_height / 2))
        draw.rectangle((x0, y0, x1, y1), fill=(255, 0, 0, 128))
        im.paste(rect, None, rect)
        draw = ImageDraw.Draw(im)
        draw.line((x0, y0, x1, y0), fill=(255, 0, 0, 0), width=min(round(1 / zoom_scale), 1) * 10)
        draw.line((x0, y0, x0, y1), fill=(255, 0, 0, 0), width=min(round(1 / zoom_scale), 1) * 10)
        draw.line((x1, y0, x1, y1), fill=(255, 0, 0, 0), width=min(round(1 / zoom_scale), 1) * 10)
        draw.line((x0, y1, x1, y1), fill=(255, 0, 0, 0), width=min(round(1 / zoom_scale), 1) * 10)
        esize = max(round(1 / zoom_scale), 1) * 5
        draw.ellipse(((focal_cx - esize, focal_cy - esize),
                      (focal_cx + esize, focal_cy + esize)), fill="#ff5555")

    # offset the crop box to keep the center of the focal point
    # in the center of the crop as much as possible
    # (this will be partially outside of the image in most cases)

    tex, tey = focal_cx - (zoomed_width / 2), focal_cy - (zoomed_height / 2)
    tfx, tfy = focal_cx + (zoomed_width / 2), focal_cy + (zoomed_height / 2)
    # move back into the image
    if tex < 0:
        # its out of the img to the left, move both to the right until tex is 0
        tfx = tfx - tex  # tex is negative!
        tex = 0
    elif tfx > source_x:
        # its out of the img to the right
        tex = tex - (tfx - source_x)
        tfx = source_x
    if tey < 0:
        # its out of the img to the top, move both to the bottom until tey is 0
        tfy = tfy - tey  # tey is negative!)
        tey = 0
    elif tfy > source_y:
        # its out of the img to the bottom
        tey = tey - (tfy - source_y)
        tfy = source_y

    # crop image
    crop_box = ((int(tex), int(tey), int(tfx), int(tfy)))
    im = im.crop(crop_box)

    # scale
    if zoom_scale < 1.0 or (zoom_scale > 1.0 and upscale):
        im = im.resize((int(zoomed_width * zoom_scale), int(zoomed_height * zoom_scale)),
                       resample=Image.ANTIALIAS)

    return im



