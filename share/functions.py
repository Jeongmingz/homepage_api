import base64
from datetime import datetime
import os

import environ
from pathlib import Path

from instaloader import Instaloader, instaloader

BASE_DIR = Path(__file__).resolve().parent.parent

def return_env_value(key: str) -> str:
	env = environ.Env()
	environ.Env.read_env(
	    env_file=os.path.join(BASE_DIR, '.env')
	)

	return env(key)


def return_login_insta_instance(id: str, pw: str) -> Instaloader:
    instance = instaloader.Instaloader()
    instance.login(id, pw)

    return instance

def post_shortcode_downloader(url: str) -> list():
    # Extract shortcode from URL
    shortcode = url.strip().split('/')[-2]
    instance = instaloader.Instaloader()

    # Load post using shortcode
    post = instaloader.Post.from_shortcode(instance.context, shortcode)

    # List to store base64-encoded images
    base64_encoding_images = []

    for i, image in enumerate(post.get_sidecar_nodes()) :
        temp_filename = "temp_image"
        instance.download_pic(temp_filename, image.display_url, datetime.now())

        with open(temp_filename+'.jpg', "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
            base64_encoding_images.append(base64_image)

    return base64_encoding_images