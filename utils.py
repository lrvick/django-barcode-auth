import hashlib
from django.contrib.auth.models import User
from django.conf import settings

try:
    from reportlab.lib.units import toLength
    from reportlab.pdfgen import canvas
    from subprocess import Popen
    import cStringIO
    from tempfile import NamedTemporaryFile
    import os.path
    import random
except ImportError:
    canvas = False


def gen_passhash(user):
    token_handle = hashlib.sha224()
    token_handle.update(user.email)
    token_handle.update(user.password)
    token_handle.update(settings.BARCODE_SECRET_KEY)
    hex_hash = token_handle.hexdigest()
    return hex_hash


def print_card(user, barcode):
    print(user)  # Don't remove this! For some reason, card printing starts using old data if you remove this. >.>; Also, it might be nice to figure out why this happens.
    PAGE_HEIGHT = toLength('2.125in')
    PAGE_WIDTH = toLength('3.37in')
    XCENTER = PAGE_WIDTH / 2.0
    YCENTER = PAGE_HEIGHT / 2.0
    pdffile = NamedTemporaryFile()
    if user.first_name:
        username = '%s %s' % (user.first_name, user.last_name)
    else:
        username = user.username

    c = canvas.Canvas(pdffile.name, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    if settings.PRINT_CARD_IMAGES:
        for img in settings.PRINT_CARD_IMAGES:
            if img['img'] == '$barcode$':
                img['img'] = barcode
            c.drawImage(img['img'], toLength(img['x']), toLength(img['y']), width=(toLength(img['width'])), height=(toLength(img['height'])), preserveAspectRatio=True)
    if settings.PRINT_CARD_TEXT:
        for msg in settings.PRINT_CARD_TEXT:
            if msg['text'] == '$username$':
                msg['text'] = username
            c.setFont(msg['font'], msg['size'])
            c.drawCentredString(toLength(msg.get('x', XCENTER)), toLength(msg.get('y', YCENTER)), msg['text'])
    c.showPage()
    if settings.PRINT_BACKS:
        if os.path.isdir(settings.PRINT_BACK_IMAGE):
            back_image = '%s/%s' % (settings.PRINT_BACK_IMAGE, random.choice(os.listdir(settings.PRINT_BACK_IMAGE)))  # This is so ugly.
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
