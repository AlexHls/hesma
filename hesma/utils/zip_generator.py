import os
import zipfile
from tempfile import SpooledTemporaryFile

from django.http import HttpResponse, StreamingHttpResponse

from config.settings.base import STREAMING_CHUNK_SIZE


class ZipFileGenerator:
    def __init__(self, selected_files, info_json=None, file_name="selected_files.zip"):
        self.selected_files = selected_files
        self.info_json = info_json
        self.file_name = file_name

    def generate_zip(self, buffer):
        # Create a zip file in the provided buffer and add selected files to it
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.selected_files:
                file_path = os.path.abspath(file_path)
                if os.path.isfile(file_path):
                    file_name = os.path.basename(file_path)
                    zipf.write(file_path, arcname=file_name)
            if self.info_json:
                zipf.writestr("info.json", bytes(self.info_json.getvalue(), "utf-8"))

    def get_response(self, streaming=False):
        """
        Create a response with the zip file content
        :param streaming: If True, create a StreamingHttpResponse. Documentation
        recommends using StreamingHttpResponse only when absolutely necessary.
        See https://docs.djangoproject.com/en/5.0/ref/request-response/#streaminghttpresponse-objects
        """
        # Use a SpooledTemporaryFile as the buffer for the zip file
        buffer = SpooledTemporaryFile()
        self.generate_zip(buffer)

        buff_size = buffer.tell()

        # Seek to the beginning of the buffer before creating the response
        buffer.seek(0)

        # Function to yield chunks from the buffer
        def file_iterator(file, chunk_size=STREAMING_CHUNK_SIZE):
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                yield data

        # Create a StreamingHttpResponse with the zip file content
        if streaming:
            response = StreamingHttpResponse(file_iterator(buffer), content_type="application/x-zip-compressed")
        else:
            response = HttpResponse(file_iterator(buffer), content_type="application/x-zip-compressed")
        response["Content-Length"] = buff_size
        response["Content-Disposition"] = f"attachment; filename={self.file_name}"
        return response
