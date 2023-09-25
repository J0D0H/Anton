import discord
import os
from dotenv import load_dotenv
from discord.ext.commands import Context
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.client.user} has connected to Discord!')
        
        
        
        
    @commands.command(name='hello', aliases=['hi'])
    @commands.guild_only()
    async def hello(self, ctx: Context):
        

        await ctx.send(
            content=(
                f"sup nigga"
            )
        )
        
        
        
async def setup(client: commands.Bot):
    await client.add_cog(Basic(client))