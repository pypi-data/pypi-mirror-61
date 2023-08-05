# boats.py
The official API wrapper for glenbotlist.xyz in Python

# Examples
## Post server count

```python
import discord
import gblpyapi.glenbotlist.GBL as GBL
import requests
from discord.ext import tasks

client = discord.Client()
gbl = GBL.GBL(token) # glenbotlist.xyz API token

@tasks.loop(minutes = 30)
async def postservers():
    await gbl.post_server_count(client.user.id, len(client.guilds))

```
