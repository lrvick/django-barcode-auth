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


def gen_passhash(user_id):
    user = User.objects.get(pk=user_id)
    token_handle = hashlib.sha224()
    token_handle.update(user.email)
    token_handle.update(user.password)
    token_handle.update(settings.SECRET_KEY)
    hex_hash = token_handle.hexdigest()
    return hex_hash


def print_card(user, barcode):
    PAGE_HEIGHT = 3.37 * inch
    PAGE_WIDTH = 2.125 * inch
    XCENTER = PAGE_WIDTH / 2.0
    pdffile = NamedTemporaryFile()
    if user.first_name:
        username = "%s %s" % (user.first_name, user.last_name)
    else:
        username = user.username

    c = canvas.Canvas(pdffile.name, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    c.drawImage(barcode, 0.19 * inch, 0.1919 * inch, width=(1.75 * inch), height=(1.75 * inch), preserveAspectRatio=True)
    c.setFont('Helvetica', 8)
    c.drawCentredString(XCENTER, 2 * inch, settings.PRINT_MESSAGE_3)
    c.setFont('Helvetica-Oblique', 8)
    c.drawCentredString(XCENTER, 2.4 * inch, "Member since %s" % user.date_joined.strftime('%m/%Y'))
    c.setFont('Helvetica-Oblique', 10)
    c.drawCentredString(XCENTER, 2.6919 * inch, settings.PRINT_MESSAGE_2)
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(XCENTER, 2.9 * inch, username)
    c.setFont('Helvetica', 8)
    c.drawCentredString(XCENTER, 3.11 * inch, settings.PRINT_MESSAGE_1)
    c.showPage()
    c.save()

    try:
        printer = "-d %s" % settings.PRINTER
    except NameError:
        printer = ""

    printjob = Popen("lp -s %s %s" % (printer, pdffile.name), shell=True)
    printjob.wait()
