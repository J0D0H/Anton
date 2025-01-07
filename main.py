import asyncio
import os
import signal
import discord
from discord.ext import commands
from dotenv import load_dotenv
from dpyConsole import Console
from OpenAI.openai_integration import get_chatgpt_response  # Import the function
from AuditLog.AuditLogReader import auditEntry, handle_disconnect
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = ["A", "a"], case_insensitive=True, help_command=None, intents=intents)
console = Console(client)



# stfu python i know i turned off the program
def thread_kill(one=None, two=None):
    print("Shutting down...")
    print("Graceful shutdown complete. Goodbye.")
    os._exit(0)
signal.signal(signal.SIGINT, thread_kill)

@console.command()
async def shutdown():
    thread_kill()

@client.event
async def on_voice_state_update(member: discord.Member, bef: discord.VoiceState, cur: discord.VoiceState):
    
    if bef.channel is not None and cur.channel is None:
        await handle_disconnect(member.guild)
    

@client.event
async def on_audit_log_entry_create(entry: discord.AuditLogEntry):
    await auditEntry(entry)
    

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    print('bot online')
    async with client:
        await load_extensions()
        console.start()
        await client.start(TOKEN)
    
@client.event
async def on_ready():
    set_async_client(client)
    asyncio.create_task(renamer())
    
asyncio.run(main())