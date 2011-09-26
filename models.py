from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from barauth.utils import gen_passhash
from barauth.utils import print_card
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

    def __unicode__(self):
        return self.user.email

def user_create_barcode(sender, instance, created, **kwargs):
    instance = User.objects.get(email=instance.email)
    password_hash = gen_passhash(instance)
    qr = QRCode(8, QRErrorCorrectLevel.Q)
    qr.addData("####%s|%s" % (str(instance.pk), str(password_hash)))
    qr.make()
    im = qr.makeImage()
    temp_file = StringIO()

    # We'll take the username if we have to, but prefer first+last
    im.save(temp_file, format='png')
    barcode_contents = ContentFile(temp_file.getvalue())

    user_barcode = UserBarcode(user=instance) 
    user_barcode.barcode.save('%s.png' % str(instance.pk), barcode_contents)

    if settings.PRINT_CARDS:
        print_card(instance, user_barcode.barcode.name)
    pass

models.signals.post_save.connect(user_create_barcode, sender=User, dispatch_uid="apps.barauth.models")
