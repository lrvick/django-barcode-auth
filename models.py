from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from utils import gen_passhash
from utils import print_card
from PyQRNative import QRCode, QRErrorCorrectLevel

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class UserBarcode(models.Model):
    user = models.ForeignKey(User, unique=True)
    barcode = models.ImageField(
            upload_to='%s/img/barcodes' % settings.MEDIA_ROOT
            )


def user_create_barcode(sender, instance, created, **kwargs):
    if created:
        password_hash = gen_passhash(instance.username)
        qr = QRCode(6, QRErrorCorrectLevel.Q)
        qr.addData("####%s|%s" % (instance.username, password_hash))
        qr.make()
        im = qr.makeImage()
        temp_file = StringIO()
        # We'll take the username if we have to, but prefer first+last
        im.save(temp_file, format='png')
        barcode_contents = ContentFile(temp_file.getvalue())
        user_barcode = UserBarcode()
        user_barcode.user = instance
        user_barcode.barcode.save('%s.png' % password_hash, barcode_contents)
        if settings.PRINT_CARDS:
            if filter(lambda x: x, [instance.first_name, instance.last_name]):
                print_card("%s %s" % (instance.first_name, instance.last_name), user_barcode.barcode.name)
            else:
                print_card(instance.username, user_barcode.barcode.name)
        pass

models.signals.post_save.connect(user_create_barcode, sender=User)
