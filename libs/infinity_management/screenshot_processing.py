import io
from PIL import Image
from google.cloud import vision


client = vision.ImageAnnotatorClient()


def crop_profile(path):
    img = Image.open(path)
    (x, y) = img.size

    cropped = []
    profile_width = x * 0.25
    top = 0
    bottom = y//2
    left = int(x / 2 - 1.5 * profile_width)

    dims = [
        (0, x / 2 - 0.5 * profile_width),
        (x / 2 - 0.5 * profile_width, x / 2 + 0.5 * profile_width),
        (x / 2 + 0.4 * profile_width, x),
    ]

    for (i, (left, right)) in enumerate(dims):
        profile = img.crop((left, top, right, bottom))
        buf = io.BytesIO()
        profile.save(buf, format="png")

        buf.seek(0)
        cropped.append(buf.read())

    return cropped


def detect_text(img, debug=False):
    """Detects text in the image buffer."""
    image = vision.types.Image(content=img)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    debug_list = []

    best = ''
    for text in texts:
        if debug:
            debug_list.append(text)

        if len(text.description) > len(best):
            best = text.description

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    if debug:
        return debug_list
    else:
        return best


def process_screenshot(target_image, debug=False):
    cropped_images = crop_profile(target_image)
    name_list = []
    for image in cropped_images:
        name_text = detect_text(image, debug)

        if len(name_text) > 0:
            name_list.append(name_text)

    return name_list
