import hashlib
from django.contrib.auth.models import User
from django.conf import settings

try:
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from subprocess import Popen
    import cStringIO
    from tempfile import NamedTemporaryFile
except ImportError:
    canvas = False


def gen_passhash(username):
    user = User.objects.get(username=username)
    token_handle = hashlib.sha224()
    token_handle.update(username)
    token_handle.update(user.password)
    token_handle.update(settings.SECRET_KEY)
    hex_hash = token_handle.hexdigest()
    return hex_hash

def print_card(username, qrcode):
        PAGE_HEIGHT = 3.37 * inch
        PAGE_WIDTH = 2.125 * inch
        XCENTER = PAGE_WIDTH / 2.0
        pdffile = NamedTemporaryFile()

        c = canvas.Canvas(pdffile.name, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        c.drawInlineImage(qrcode, 0.19 * inch, 0.1919 * inch, width=(1.75 * inch), height=(1.75 * inch), preserveAspectRatio=True)
        c.setFont('Helvetica', 8)
        c.drawCentredString(XCENTER, 2.1919 * inch, 'SCAN AT THE STATIONS')
        c.setFont('Helvetica-Oblique', 10)
        c.drawCentredString(XCENTER, 2.6919 * inch, 'MAYO INSIDER')
        c.setFont('Helvetica-Bold', 14)
        c.drawCentredString(XCENTER, 2.9 * inch, username)
        c.setFont('Helvetica', 8)
        c.drawCentredString(XCENTER, 3.11 * inch, "WELCOME")
        c.showPage()
        c.save()

        try:
            printer = "-d %s" % settings.PRINTER
        except NameError:
            printer = ""

        printjob = Popen("lp %s %s" % (printer, pdffile.name), shell=True)
        printjob.wait()
