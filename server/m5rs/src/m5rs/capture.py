from io import BytesIO
from Xlib import display
from PIL import Image
import Xlib.X

dsp = display.Display()

def capture_window(window_id=0):
    if window_id == 0:
        window = dsp.screen().root
    else:
        window = dsp.create_resource_object('window', window_id)

    geom = window.get_geometry()
    width = geom.width
    height = geom.height

    raw = window.get_image(0, 0, width, height, Xlib.X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (width, height), raw.data, "raw", "BGRX")
    return image

def resize_image(image, width, height):
    original_width, original_height = image.size
    ratio = min(width / original_width, height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    result = Image.new("RGB", (width, height), (0, 0, 0))
    offset_x = (width - new_width) // 2
    offset_y = (height - new_height) // 2
    result.paste(resized_image, (offset_x, offset_y))
    return result

def image_to_jpeg_bytes(image, quality=85) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    return buffer.getvalue()

if __name__ == "__main__":
    import sys
    image = None
    if len(sys.argv) > 1:
        window_id = int(sys.argv[1], 16)
        image = capture_window(window_id)
    else:
        image = capture_window()
    resized_image = resize_image(image, 240, 135)
    resized_image.save("output.jpg", format="JPEG")
