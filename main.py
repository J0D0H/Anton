import asyncio
import os
import signal
import discord
import time
from discord.ext import commands
from dotenv import load_dotenv
from dpyConsole import Console
from OpenAI.openai_integration import get_chatgpt_response  # Import the function
from AuditLog.AuditLogReader import auditEntry, handle_disconnect
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

last_api_call = time.time()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = ["A", "a"], case_insensitive=True, help_command=None, intents=intents)
console = Console(client)

async def shutdown_bot():
    await client.close()  # Close the bot connection gracefully

# Handle shutdown signal
def thread_kill(one=None, two=None):
    print("Shutting down...")
    asyncio.create_task(shutdown_bot())  # Schedule the shutdown coroutine
    print("Graceful shutdown initiated.")

signal.signal(signal.SIGINT, thread_kill)

@console.command()
async def shutdown():
    await shutdown_bot()  # Shutdown through console command

@client.event
async def on_ready():
    print(f'{client.user.name} is connected and ready!')

@client.event
async def on_message(message):
    global last_api_call
    print(f"Received message: {message.content}")  # Debugging log

    if message.author == client.user:
        return  # Ignore messages from the bot itself

        # Check if the message has an attachment
    if message.attachments:
        for attachment in message.attachments:
            # Check if the attachment is a text file (or any file you want to handle)
            if attachment.filename.endswith('.txt'):  # You can add more file types if needed
                # Download the file
                file_data = await attachment.read()
                file_content = file_data.decode('utf-8')  # Decode the file content

                # Process the file content (e.g., send it to ChatGPT or log it)
                await message.channel.send(f"Received a file: {attachment.filename}")
                await message.channel.send(f"File content:\n```\n{file_content[:1000]}\n```")  # Send first 1000 chars for preview

                # Optionally, save the file locally
                with open(attachment.filename, "wb") as f:
                    f.write(file_data)

                await message.channel.send(f"File saved as `{attachment.filename}`.")

    # Check if the bot was mentioned
    if client.user.mentioned_in(message):
        current_time=time.time()
        if current_time - last_api_call < 5: 
            await message.channel.send("wait fool")
            return
        last_api_call = current_time

        user_message = message.content  # Get the full message content
        
        await message.channel.send("Processing your request...")  # Inform user
        
        # Generate a response using OpenAI
        ai_response = get_chatgpt_response(user_message)  # Get the AI response
        
        if len(ai_response) > 3999:
            # Create a text file with the response
            with open("response.txt", "w", encoding="utf-8") as file:
                file.write(ai_response)
            
            # Send the file to the channel
            await message.channel.send(file=discord.File("response.txt"))
            
            # Optionally, delete the file after sending
            os.remove("response.txt")
        else:
            # Send the AI response back in the channel
            await message.channel.send(ai_response)

async def load_extensions():
    # Load any cog extensions if you're using them
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    print('Bot online')
    await load_extensions()  # Load extensions initially
    await client.start(TOKEN)  # Start the bot with the token

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())  # Start the bot