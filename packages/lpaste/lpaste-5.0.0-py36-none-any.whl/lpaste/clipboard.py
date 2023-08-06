import sys
import struct
import io
import contextlib

import jaraco.clipboard

from .source import FileSource, CodeSource


def get_image():
    try:
        from PIL import Image
    except ImportError:
        print("PIL not available - image pasting disabled", file=sys.stderr)
        raise
    result = jaraco.clipboard.paste_image()
    # construct a header (see http://en.wikipedia.org/wiki/BMP_file_format)
    offset = 54  # 14 byte BMP header + 40 byte DIB header
    header = b'BM' + struct.pack('<LLL', len(result), 0, offset)
    img_stream = io.BytesIO(header + result)
    img = Image.open(img_stream)
    out_stream = io.BytesIO()
    img.save(out_stream, format='jpeg')
    out_stream.seek(0)
    return out_stream, 'image/jpeg', 'image.jpeg'


def try_until_no_exception(*functions):
    for f in functions:
        exceptions = getattr(f, 'exceptions', ())
        with contextlib.suppress(exceptions):
            return f()
    raise RuntimeError("No function succeeded")


def do_image():
    return FileSource(*get_image())


def do_html():
    value = jaraco.clipboard.paste_html()
    if value is None:
        raise ValueError("No HTML value")
    return FileSource.from_snippet(value)


def do_text():
    code = jaraco.clipboard.paste_text()
    src = CodeSource(code)
    src.check_python()
    return src


def get_source():
    """
    Return lpaste.Source for the content on the clipboard
    """
    # try getting an image or html over just text
    do_image.exceptions = TypeError, ImportError, NotImplementedError
    do_html.exceptions = TypeError, ValueError
    return try_until_no_exception(do_image, do_html, do_text)


set_text = jaraco.clipboard.copy_text
