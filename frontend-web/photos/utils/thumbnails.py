import os

from django.conf import settings
from PIL import Image, ImageOps

from photos.utils.metadata import PhotoMetadata


def generate_thumbnail(photo, size=256, aspect='square'):
    pf = photo.files.filter(mimetype='image/jpeg')[0]
    im = Image.open(pf.path)

    if im.mode != 'RGB':
        im = im.convert("RGB")

    im = ImageOps.fit(im, (size, size), Image.ANTIALIAS)
    metadata = PhotoMetadata(pf.path)

    if metadata.get('Orientation') in ['Rotate 90 CW', 'Rotate 270 CCW']:
        im = im.rotate(-90, expand=True)
    elif metadata.get('Orientation') in ['Rotate 90 CCW', 'Rotate 270 CW']:
        im = im.rotate(90, expand=True)

    path = os.path.join(settings.THUMBNAIL_ROOT, '{}.jpg'.format(photo.id))
    im.save(path, format='JPEG', quality=50)