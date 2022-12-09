from logging import INFO, FileHandler, StreamHandler, basicConfig, error, info
from os import environ, path, remove
from platform import machine
from subprocess import run

from dotenv import load_dotenv
from pymongo import MongoClient
from requests import request

if path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[FileHandler('log.txt'), StreamHandler()],
                    level=INFO)

load_dotenv('config.env', override=True)

try:
    if bool(environ.get('_____REMOVE_THIS_LINE_____')):
        error('The README.md file there to be read! Exiting now!')
        exit()
except:
    pass

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = int(BOT_TOKEN.split(':', 1)[0])

DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = None

if DATABASE_URL:
    conn = MongoClient(DATABASE_URL)
    db = conn.mltb
    if config_dict := db.settings.config.find_one({'_id': bot_id}):  #retrun config dict (all env vars)
        environ['UPSTREAM_REPO'] = config_dict['UPSTREAM_REPO']
        environ['UPSTREAM_BRANCH'] = config_dict['UPSTREAM_BRANCH']
    conn.close()

load_dotenv('config.env', override=True)

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = 'https://github.com/junedkh/jmdkh-mltb'

UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', '')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'master'

if path.exists('.git'):
    run(["rm", "-rf", ".git"])

update = run([f"git init -q \
                    && git config --global user.email kjuned007@gmail.com \
                    && git config --global user.name junedkh \
                    && git add . \
                    && git commit -sm update -q \
                    && git remote add origin {UPSTREAM_REPO} \
                    && git fetch origin -q \
                    && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

if update.returncode == 0:
    info('Successfully updated with latest commit from UPSTREAM_REPO')
else:
    error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')

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