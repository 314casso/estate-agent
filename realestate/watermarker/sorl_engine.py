#!/usr/bin/env python
# vim:fileencoding=utf-8

from django.conf import settings
from watermarker import watermark
from sorl.thumbnail.engines.pil_engine import Engine

__author__ = 'zeus'

WATERMARK_OPTIONS = getattr(settings, 'WATERMARK_OPTIONS', {
    'font_path': 'tahoma.ttf',
    'font_scale': 0.05,
})

WATERMARK_MIN_SIZE = getattr(settings, 'WATERMARK_MIN_SIZE', 150)
WATERMARK_FORCE = getattr(settings, 'WATERMARK_FORCE', False)

class WatermarkEngine(Engine):
    '''
    Add watermark to sorl.thumbnail pil engine
    '''
    def create(self, image, geometry, options):
        image = super(WatermarkEngine, self).create(image, geometry, options)
        if 'watermark' in options or WATERMARK_FORCE:
            text = options.get('watermark', WATERMARK_FORCE)
            if max(geometry)>WATERMARK_MIN_SIZE:
                image = watermark(image, text ,**WATERMARK_OPTIONS)
        return image
  