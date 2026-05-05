import os

from django.http import Http404


def existing_file_path(file_field, missing_message):
    if not file_field:
        raise Http404(missing_message)

    path = file_field.path
    if not os.path.isfile(path):
        raise Http404(missing_message)
    return path
