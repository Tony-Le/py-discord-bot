import requests


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False


def add_image_file_extension_if_none(filename, content_type):
    if not (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg')):
        if content_type == "image/png":
            filename += '.png'
        elif content_type == "image/jpeg":
            filename += '.jpeg'
        elif content_type == "image/jpg":
            filename += '.jpg'
    return filename
