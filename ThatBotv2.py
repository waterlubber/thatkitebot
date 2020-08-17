"""
MIT License

Copyright (c) 2020 ThatRedKite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
from datetime import datetime
from bf.yamler import Tomler
from discord.ext import commands, tasks
from bf.util import colors,clear_temp_folder
import cogs
import os
from pathlib import Path
import aiohttp
import gc

dirname=Path(os.path.dirname(os.path.realpath(__file__)))

if not dirname.joinpath("data","temp").exists():
    print(colors.red+f"    temp directory not found,creating temp directory")
    os.mkdir(dirname.joinpath("data","temp"))

tempdir=dirname.joinpath("data","temp")
tom=Tomler(dirname)
prefix=tom.prefix
discordtoken=tom.token
tenortoken=tom.tenortoken
if tenortoken is None or tenortoken=="":
    print(colors.red+colors.bold+colors.underlined+f"*** tenor token not found! Cannot use features that use tenor! ***{colors.clear}")

# clean up some shit
clear_temp_folder(dirname)

class ThatKiteBot(commands.Bot):
    def __init__(self,command_prefix,dirname,help_command=None,description=None,**options):
        super().__init__(command_prefix, help_command=help_command, description=description, **options)
        # ---static values---
            
            #paths
        self.dirname=dirname
        self.tempdir=self.dirname.joinpath("data","temp")

            #info
        self.version="b23"
        self.tom=Tomler(dirname)
        self.starttime=datetime.now()
        self.pid=os.getpid()

        # ---dynamic values---

            #settings
        self.settings=tom.settings_all

            #sessions
        self.loop.run_until_complete(self.aiohttp_start())
    
    async def aiohttp_start(self):
        self.aiohttp_session=aiohttp.ClientSession()

    @tasks.loop(seconds=5.0)
    async def garbage(self):
        gc.collect()
        print("gc run")
        
print("initilizing bot . . .")        
bot=ThatKiteBot(prefix,dirname)
bot.remove_command("help")

#cogs
bot.add_cog(cogs.funstuffcog.fun_stuff(bot,dirname))
bot.add_cog(cogs.musiccog.music(bot,dirname))
bot.add_cog(cogs.imagecog.image_stuff(bot))
bot.add_cog(cogs.nsfwcog.NSFW(bot))
bot.add_cog(cogs.listenercog.listeners(bot,dirname))
bot.add_cog(cogs.sudocog.sudo_commands(bot,dirname))
bot.add_cog(cogs.utilitiescog.utility_commands(bot,dirname))
gc.enable()

loop=asyncio.get_event_loop()
bot.case_insensitive=True

loop.run_until_complete(bot.start(discordtoken))

