from PyQRNative import QRCode, QRErrorCorrectLevel
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from reportlab.lib.units import toLength
from reportlab.pdfgen import canvas
from subprocess import Popen
from tempfile import NamedTemporaryFile
import hashlib
import os.path
import random


def gen_passhash(user):
    token_handle = hashlib.sha224()
    token_handle.update(user.email)
    token_handle.update(user.password)
    token_handle.update(settings.BARCODE_SECRET_KEY)
    hex_hash = token_handle.hexdigest()
    return hex_hash


def print_card(instance, **kwargs):
    PAGE_HEIGHT = toLength('2.125in')
    PAGE_WIDTH = toLength('3.37in')
    XCENTER = PAGE_WIDTH / 2.0
    YCENTER = PAGE_HEIGHT / 2.0
    pdffile = NamedTemporaryFile(delete=True)

    # Generate the QR Code
    user = User.objects.get(email=instance.email)
    password_hash = gen_passhash(user)
    qr = QRCode(8, QRErrorCorrectLevel.Q)
    qr.addData("####%s|%s" % (str(user.pk), str(password_hash)))
    qr.make()
    im = qr.makeImage()
    # ^^^^ Reportlab seems to not accept this type of PIL object,
    # so I'm using a temp file. I'd use StringIO, but reportlab tries to parse
    # a path for the file. It seems it doesn't accept file objects, it wants a
    # path or a PIL object that...isn't the same as the
    # one makeImage() gives us.
    temp_file = NamedTemporaryFile(delete=True)
    im.save(temp_file, format='png')

    # We'll take the username if we have to, but prefer first+last
    if user.first_name:
        username = '%s %s' % (user.first_name, user.last_name)
    else:
        username = user.username

    c = canvas.Canvas(pdffile.name, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    if hasattr(settings, 'PRINT_CARD_IMAGES'):
        for img in settings.PRINT_CARD_IMAGES:
            c.drawImage(temp_file.name if img['img'] == '$barcode$' else
                    img['img'], toLength(img['x']), toLength(img['y']),
                    width=(toLength(img['width'])),
                    height=(toLength(img['height'])), preserveAspectRatio=True)

    if hasattr(settings, 'PRINT_CARD_TEXT'):
        for msg in settings.PRINT_CARD_TEXT:
            c.setFont(msg['font'], msg['size'])
            c.drawCentredString(toLength(msg.get('x', XCENTER)),
                    toLength(msg.get('y', YCENTER)), username if
                    msg['text'] == '$username$' else msg['text'])

    c.showPage()
    if hasattr(settings, 'PRINT_BACK_IMAGE'):
        # If a directory is given for back images, choose randomly
        if os.path.isdir(settings.PRINT_BACK_IMAGE):
            back_image = '%s/%s' % (settings.PRINT_BACK_IMAGE,
                    random.choice(os.listdir(settings.PRINT_BACK_IMAGE)))
        # Otherwise, expect an image path
        elif os.path.isfile(settings.PRINT_BACK_IMAGE):
            back_image = settings.PRINT_BACK_IMAGE
        c.drawImage(back_image, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
        c.showPage()
    c.save()

    try:
        printer = '-d %s' % settings.PRINTER
    except NameError:
        printer = ''

    printjob = Popen('lp -s %s %s' % (printer, pdffile.name), shell=True)
    printjob.wait()

if settings.PRINT_CARDS:
    models.signals.post_save.connect(print_card, sender=User, weak=False,
            dispatch_uid="apps.barauth.utils")
