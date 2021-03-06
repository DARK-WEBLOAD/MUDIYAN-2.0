

from pyrogram import Client, filters

import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
import time

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------

@Client.on_message(filters.command("song") & ~filters.channel & ~filters.edited)
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`๐ป๐ญ๐๐๐๐๐๐ ๐๐๐๐ ๐๐๐๐๐ถ.....`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[แดแดสแด แดกแดสสแดแดแด แดแดsษชแด]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**๐ ๐๐ฆ ๐ง๐จ๐ญ ๐๐จ๐ฎ๐ง๐ ๐ซ๐๐ฌ๐ฎ๐ฅ๐ญ ๐ข๐ง ๐ฒ๐จ๐ฎ๐ซ ๐ซ๐๐ช๐ฎ๐๐ฌ๐ญ๐. ๐๐ฅ๐๐๐ฌ๐ ๐ญ๐ซ๐ฒ ๐๐ง๐จ๐ญ๐ก๐๐ซ ๐ฌ๐จ๐ง๐? ๐จ๐ซ ๐ฎ๐ฌ๐ ๐๐จ๐ซ๐ซ๐๐๐ญ ๐ฌ๐ฉ๐๐ฅ๐ฅ๐ข๐ง๐?๐!**')
            return
    except Exception as e:
        m.edit(
            "**๐๐ง๐ญ๐๐ซ ๐๐จ๐ง๐? ๐๐๐ฆ๐ ๐ฐ๐ข๐ญ๐ก ๐๐จ๐ฆ๐ฆ๐๐ง๐๐**โ\nFor ๐๐ฑ๐๐ฆ๐ฉ๐ฅ๐: `/song Alone Marshmellow`"
        )
        print(str(e))
        return
    m.edit("`๐ผ๐๐๐๐๐๐๐๐๐ป....๐๐๐๐๐๐ ๐๐๐๐๐`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'๐น <b>๐ป๐๐๐๐:</b> <a href="{link}">{title}</a>\n๐๏ธ <b>๐ซ๐๐๐๐๐๐๐:</b> <code>{duration}</code>\n๐ต <b>๐ฝ๐๐๐๐:</b> <code>{views}</code>\n๐ป <b>๐น๐๐๐๐๐๐๐๐ ๐๐:</b> {message.from_user.mention()} \n๐ถ <b>๐ผ๐๐๐๐๐๐๐ ๐ฉ๐: @NewOTTmoviesAll</b> ๐'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**๐๐ง ๐๐ซ๐ซ๐จ๐ซ ๐๐๐๐ฎ๐ซ๐๐. ๐๐ฅ๐๐๐ฌ๐ ๐๐๐ฉ๐จ๐ซ๐ญ ๐๐ก๐ข๐ฌ ๐๐จ @DARKWEBLOAD !!**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
