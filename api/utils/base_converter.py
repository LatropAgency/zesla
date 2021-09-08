import abc

import base64

import imgkit
import pdfkit
from django.http import HttpResponse

from api.models import File


class BaseConverter(metaclass=abc.ABCMeta):
    def __init__(self, file: File):
        self.file = file

    @staticmethod
    def _get_html(body):
        return """
                <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                    </head>
                    <body>
                        %s
                    </body>
                </html>
            """ % body

    def _prepare_html(self):
        base64_file = self.file.data.tobytes().decode('utf-8')
        decoded_file = base64.b64decode(base64_file).decode('utf-8')
        return self._get_html(decoded_file)

    def get_response(self, converted_object: bytes, name: str) -> HttpResponse:
        response = HttpResponse(converted_object, content_type=self.content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % name
        return response

    @abc.abstractmethod
    def convert(self):
        pass

    @abc.abstractmethod
    def content_type(self):
        pass


class PngConverter(BaseConverter):
    content_type = 'application/png'

    def convert(self):
        return imgkit.from_string(self._prepare_html(), False, options={'format': 'png'})


class PdfConverter(BaseConverter):
    content_type = 'application/pdf'

    def convert(self):
        return pdfkit.from_string(self._prepare_html(), False)
