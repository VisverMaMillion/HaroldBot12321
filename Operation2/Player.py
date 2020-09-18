import discord
from discord.ext import commands, tasks
from discord.utils import get
import urllib.parse
import urllib.request
import re
import random as rd
import numpy as np
import os
import youtube_dl
# ##################################################
workdir = os.path.dirname(__file__)
songdir = os.path.join(workdir, 'songs')
playlistdir = os.path.join(workdir, 'playlists')
songdowndir = os.path.join(workdir, 'songs/%(title)s.%(ext)s')
queue = np.array([])
length = np.array([])
urlque = np.array([])
result = np.array([])
kello = 0
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': songdowndir
}


def queclr(y, x):  # works
    global queue
    global urlque
    if y == 0:
        try:
            for song in os.listdir(songdir):
                filepath = os.path.join(songdir, song)
                os.unlink(filepath)
        except error:
            pass
    elif y == 1:
        try:  # tuhoutuu joskus
            filepath = os.path.join(songdir, queue[0] + '.mp3')
            queue = np.delete(queue, 0)
            urlque = np.delete(urlque, 0)
            os.unlink(filepath)
        except IndexError:
            print('sire, thou art gay')
            pass

    elif y == 2:
        try:
            urlque = np.delete(urlque, x)
        except IndexError:
            print('enemy sighted')
            pass


def get_title(url):
    global ydl_opts
    global length

    #   if title.size == 0:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)
    #        lengthval = info_dict.get('duration', None) #turha?
    if title.count(':') >= 1:
        title = title.replace(':', ' -')
    if title.count('|') >= 1:
        title = title.replace('|', '_')
    if title.count('/') >= 1:
        title = title.replace('/', '_')
    if title.count('"') >= 1:
        title = title.replace('"', '\'')

    return title


def firsturl():
    se = urlque[0]
    return se


def urlfromque():  # works deletes too early
    queclr(1, 1)
    try:
        se = urlque[0]
        return se
    except IndexError:
        return None


def songdload(url):  # works , lisää search, mieti saako queen nimet
    global queue
    global kello
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading song\n')
            ydl.cache.remove()
            ydl.download([url])
            ntitle = get_title(url)
            queue = np.append(queue, ntitle)
            kello = 0

    except error:
        if kello <= 3:
            print('REEE')
            kello += 1
            songdload(url)
        else:
            kello = 0
            return
    return

