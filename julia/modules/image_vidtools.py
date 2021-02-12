from julia.Config import Config
from julia.events import register
from julia import CMD_HELP
from julia import tbot as borg
from julia import TEMP_DOWNLOAD_DIRECTORY
import os
import wget
from shutil import rmtree
import cv2
import cv2 as cv
import random
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pytz 
import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
from telegraph import upload_file
import time
import html
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
sedpath = "./starkgangz/"
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)
from julia.Ok import upload_file as uf
from julia.func import convert_to_image, crop_vid, runcmd, tgs_to_gif

