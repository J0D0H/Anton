import asyncio
import discord

client: discord.Client = None
def set_async_client(c):
    global client
    client = c

async def renamer():
    while True:
        ATesting = await client.fetch_channel(1155982987440160868)
        for i in range(0,19):
            await ATesting.send(content= "NIGGER BITCH CUNT ASS RETARDED FUCKHEAD DICK FAGGOT NIGGA WETBACK SLUT ZIPPERHEAD WHORE THE A MOMMY DADDY I'M GAY TWAT PUSSY WANKER DYKE DAMN CUM CUMMING SOCK")
            await asyncio.sleep(1)
        await asyncio.sleep(3600)
        
