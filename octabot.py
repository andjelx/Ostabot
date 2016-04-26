import sys
import asyncio
import subprocess
import telepot
import telepot.async
from telepot.async.delegate import per_chat_id, per_message, create_open, call
from pprint import pprint

# Global variables
SCRIPTPATH = '/home/bsod/ostabot/'
CACHEPATH = SCRIPTPATH + 'cache/'
OUTPATH = SCRIPTPATH + 'out/'
"""
$ python3.4 countera.py <token>
Count number of messages. Start over if silent for 10 seconds.
"""

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


class MessageCounter(telepot.async.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(MessageCounter, self).__init__(seed_tuple, timeout)
        self._count = 0
        self._seen = set()

    @asyncio.coroutine
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print('Chat:', content_type, chat_type, chat_id)
      
        if self._count == 1:
          yield from self.sender.sendMessage('Already processing. Be patient')
          return

        if content_type == 'photo':
          file_id = msg['photo'][-1]['file_id']
          print(file_id)
          self._seen.add(file_id)
          yield from bot.download_file(file_id, CACHEPATH + file_id)
        else:
          yield from self.sender.sendMessage('Feed me with two photos at once ^_^')

        if len(self._seen) == 2:
          self._count = 1
          yield from self.sender.sendMessage('I got two photos - wait few minutes...')
          print(self._seen)

          outfile = str(chat_id)+'.png'
          command = '/home/bsod/ostabot/th.sh'.split()
          for e in self._seen:
            command.append(CACHEPATH + e)
          command.append('100')
          command.append(outfile)
          self._seen.clear()

          for l in run_command(command):
            print(l)

          f = open(OUTPATH + outfile, 'rb')
          yield from self.sender.sendMessage('Done')
          yield from bot.sendPhoto(chat_id, f)
          self._count = 0

# Do some simple stuff for every message, to be paired with per_message()
def simple_function(seed_tuple):
    bot, msg, id = seed_tuple
    content_type, chat_type, chat_id = telepot.glance(msg)
"""
    if content_type == 'photo':
      file_id = msg['photo'][-1]['file_id']
      print(file_id)
      print(msg)
      print('------')
#      pprint(bot)
      yield from bot.download_file(file_id, CACHEPATH+'down.1')
"""

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.async.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(MessageCounter, timeout=10)),
    (per_message(), call(simple_function)),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()