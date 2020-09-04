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


def detect_text(img):
    """Detects text in the image buffer."""
    image = vision.types.Image(content=img)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    best = ''
    for text in texts:
        if len(text.description) > len(best):
            best = text.description

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return best


def process_screenshot(target_image):
    cropped_image = crop_profile(target_image)
    print(detect_text(cropped_image))


# if __name__ == "__main__":
#     import sys
#     import os
#     import os.path as path
#
#     if len(sys.argv) < 3:
#         print("Usage: ocr.py <output csv file> <image file or directory of images>")
#         exit(1)
#
#     exists = path.isfile(sys.argv[1])
#     output = open(sys.argv[1], 'r+')
#     data = {}
#     csv_data = csv.reader(output)
#     for row in csv_data:
#         data[(row[0], row[1])] = row
#
#     dir = sys.argv[2]
#     files = [dir]
#     if path.isdir(dir):
#         files = [f for f in os.listdir(dir) if path.isfile(path.join(dir, f))]
#     output.seek(0, 2)
#
#     if not exists:
#         print('discord_id,timestamp,name1,name2,name3', file=output)
#     for f in files:
#         (discord_id, timestamp, counter) = f.split('-')
#         if counter == '1' and (discord_id, timestamp) in data:
#             continue
#         images = crop_profile(path.join(dir, f))
#         names = []
#         for img in images:
#             names.append(detect_text(img).strip())
#         print(f'{discord_id},{timestamp},{names[0]},{names[1]},{names[2]}',
#               file=output, flush=True)
