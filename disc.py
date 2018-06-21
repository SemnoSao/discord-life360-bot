import os
import discord
import life360_api
import maps

LIFE360_TOKEN = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="
DISCORD_TOKEN = os.environ["disc_key"]
LIFE360_usr = os.environ["life360_usr"]
LIFE360_psw = os.environ["life360_psw"]

client = discord.Client()
api_life360 = life360_api.life360(LIFE360_TOKEN, LIFE360_usr, LIFE360_psw)
autenticado = False

if api_life360.authenticate():
    circles = api_life360.get_circles()
    c_id = circles[0]['id']
    circle = api_life360.get_circle(c_id)
    autenticado = True


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('>') or message.content.endsswith(', porra'):
        if message.content.startswith('>ajude') or message.content.startswith('>a') or message.content.startswith('ajude'):
            with open("help.txt") as h:
                msg = h.read()
            await client.send_message(message.channel, msg)
        elif message.content.startswith('>cade') or message.content.startswith('>c') or message.content.startswith('cade'):
            if autenticado:
                msg = "**Erro:**\n```Membro não encontrado```"
                nome = " ".join(message.content.split()[
                                1:]).lower().split(",")[0]
                for m in circle['members']:
                    if nome == m['firstName'].lower():
                        results = maps.retornarEnd(
                            m['location']['latitude'] + "," + m['location']['longitude'])
                        msg = "**Última localização de " + \
                            m['firstName'] + ":**\n" + results[1]
                await client.send_message(message.channel, msg)
            else:
                await client.send_message(message.channel, "**Erro:**\n```Autenticação de login inválida```")
        elif message.content.startswith('>liste') or message.content.startswith('>l') or message.content.startswith('liste'):
            if autenticado:
                msg = "**Lista de membros em " + circle['name'] + ":**```"
                for m in circle['members']:
                    msg += "\n・" + m['firstName']
                msg += "```"
                await client.send_message(message.channel, msg)
            else:
                await client.send_message(message.channel, "**Erro:**\n```Autenticação de login inválida```")
        else:
            await client.send_message(message.channel, "**Erro:**\n```Comando Não reconhecido\nEscreva >help para uma lista dos comando disponíveis```")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=">help"))

client.run(DISCORD_TOKEN)
