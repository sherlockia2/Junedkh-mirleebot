from logging import error, info
from os import path, remove
from platform import machine
from subprocess import run

from requests import request

if not path.isfile('.jmdkh'):
    try:
        res = request('GET', f"https://github.com/junedkh/jmdkh-mltb/releases/latest/download/jmdkh_mltb_{machine()}.zip")
        if res.status_code == 200:
            info("Downloading important files....")
            with open('jmdkh.zip', 'wb+') as f:
                f.write(res.content)
            info("Extracting important files....")
            run(["unzip", "-q", "-o", "jmdkh.zip"])
            run(["chmod", "-R", "777", "bot"])
            info("Ready to Start!")
            with open('.jmdkh', 'w') as f:
                f.write("DO NOT DELETE ME!")
            remove("jmdkh.zip")
        else:
            error(f"Failed to download jmdkh.zip, link got HTTP response: {res.status_code}")
    except Exception as e:
        error(f"Release url : {e}")