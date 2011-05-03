from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from PyQRNative import QRCode, QRErrorCorrectLevel 
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
 
class UserBarcode(models.Model):
    user = models.ForeignKey(User, unique=True)
    barcode = models.ImageField(upload_to='%s/img/barcodes' % settings.STATIC_ROOT)
    def save(self):
        if not self.barcode:
            password_hash = self.user.password
            qr = QRCode(5, QRErrorCorrectLevel.Q)
            qr.addData(password_hash)
            qr.make()
            im = qr.makeImage()
            temp_file = StringIO()
            im.save(temp_file, format='png')
            barcode_contents = ContentFile(temp_file.getvalue())
            self.barcode.save('%s.png' % password_hash,barcode_contents)
            super(UserBarcode, self).save()
