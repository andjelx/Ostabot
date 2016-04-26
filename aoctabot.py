import sys
import asyncio
import random
import telepot
import telepot.async
import subprocess
from telepot.async.delegate import per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

"""
$ python3.4 skeletona.py <token>
A skeleton for your async telepot programs.
"""

message_with_inline_keyboard = None

#@asyncio.coroutine
def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


@asyncio.coroutine
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'photo':
      yield from bot.sendMessage(chat_id, 'Feed me with two photos ^_^')
    
    print(msg)
#    print(self._count)

#    cmd = msg['text'].lower()
    
#    command = msg['text'][-1:].lower()
#    yield from bot.sendMessage(chat_id, 'Started...')
"""
    outfile = str(chat_id)+'.png'
    command = '/home/bsod/ostabot/th.sh cache/the_scream.jpg cache/brad_pitt.jpg 10'.split()
    command.append(outfile)
    for line in run_command(command):
        print(line)
    f = open('/home/bsod/ostabot/out/'+outfile, 'rb')
    yield from bot.sendMessage(chat_id, 'Ta dam!')
    yield from bot.sendPhoto(chat_id, f)
"""

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.async.Bot(TOKEN)
#bot = telepot.async.DelegatorBot(TOKEN, [ 
#    (per_chat_id(), create_open(MessageCounter, timeout=10)),
#])

answerer = telepot.async.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': on_chat_message }))
print('Listening ...')

loop.run_forever()