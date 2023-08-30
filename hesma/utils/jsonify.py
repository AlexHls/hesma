import json


def json_make_save(json_object):
    """
    This will escape all the HTML/XML special characters with their unicode
    escapes.
    """

    json_str = json.dumps(json_object)

    # Escape all the XML/HTML special characters.
    escapes = ["<", ">", "&"]
    for c in escapes:
        json_str = json_str.replace(c, r"\u%04x" % ord(c))

    # now it's safe to use mark_safe
    return json_str
