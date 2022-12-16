from django import template
from django.http import HttpResponse
from django.conf import settings
import os

# Customer Template Tags

register = template.Library()

@register.simple_tag
def download_file(filename):
    file_dir = os.path.join(settings.MEDIA_ROOT, f'{filename}.pdf')
    if os.path.exists(file_dir):
        with open(file_dir, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_dir)
            return response
