import requests
import asyncio
from twitchio.ext import commands
from flask import Flask
from threading import Thread
import random


# Configuración de la API de Twitch
CLIENT_ID = 'k8yfdebo8kbbljxwuqjd1d253nuifv'  # Coloca tu Client ID aquí
ACCESS_TOKEN = 'p9jj84mbhkrjn02xeow3ja5u7euu5l'  # Coloca tu Access Token aquí
CHANNELS = ['aldimirco', 'baulo', 'florchus', 'chabon', 'illojuan', 'julianpz7', 'harryalexok', 'josedeodo', 'goncho', 'duendepablo', '0kempes', 'xqc']  # Lista de canales a monitorear
API_URL = "https://api.twitch.tv/helix/streams?user_login="

# Código del bot de Twitch
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token='p9jj84mbhkrjn02xeow3ja5u7euu5l',
                         prefix='!',
                         initial_channels=['daantesiito'])
        self.live_status = {channel: False for channel in CHANNELS}  # Estado de cada canal (en vivo o no)

    async def event_ready(self):
        print(f'Conectado como {self.nick}')
        await self.check_channels_live()

    # Verificar cada cierto tiempo si los canales están en directo
    async def check_channels_live(self):
        while True:
            for channel in CHANNELS:
                live_status = is_channel_live(channel)
                if live_status and not self.live_status[channel]:
                    self.live_status[channel] = True
                    notify_channel = self.get_channel('daantesiito')  # Canal donde se enviará el mensaje
                    await notify_channel.send(f"/me prendio {channel} HAPPEEEE @daantesiito")
                elif not live_status and self.live_status[channel]:
                    self.live_status[channel] = False  # Resetear el estado si el canal ya no está en directo
            await asyncio.sleep(60)  # Esperar 1 minuto antes de volver a verificar

    # Agregar el comando !hola al bot
    @commands.command(name='hola')
    async def hola(self, ctx):
        await ctx.send(f'¡Hola @{ctx.author.name}!')

    # Comando !randm
    @commands.command(name='randm')
    async def responde(self, ctx):
        # Obtener la lista de chatters en el canal
        channel = self.get_channel('daantesiito')  # El canal de Twitch donde el bot está operando
        chatters = list(channel.chatters)  # Obtener la lista de chatters
        if chatters:
            random_chatter = random.choice(chatters)  # Elegir un chatter aleatorio
            await ctx.send(f'HOLA @{random_chatter.name}')
        else:
            await ctx.send('No hay nadie en el chat en este momento.')

# Función para verificar si un canal está en vivo
def is_channel_live(channel):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    response = requests.get(API_URL + channel, headers=headers)
    data = response.json()
    if data['data']:
        return True
    return False

# Código para mantener el bot en línea usando Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Iniciar la función keep_alive y el bot
if __name__ == "__main__":
    keep_alive()
    bot = Bot()
    bot.run()
