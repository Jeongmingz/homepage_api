import os
import environ
from pathlib import Path

from instaloader import Instaloader, LoginException

BASE_DIR = Path(__file__).resolve().parent.parent

def return_env_value(key: str) -> str:
	env = environ.Env()
	environ.Env.read_env(
	    env_file=os.path.join(BASE_DIR, '.env')
	)

	return env(key)


def return_login_insta_instance(id: str, pw: str) -> Instaloader:
    instance = Instaloader()
    instance.login(id, pw)

    return instance
