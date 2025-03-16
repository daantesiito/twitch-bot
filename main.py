import requests
import asyncio
from twitchio.ext import commands
from flask import Flask
from threading import Thread
import random
import sys
import base64

sys.stdout.reconfigure(encoding='utf-8')

# Configuración de la API de Twitch
CLIENT_ID = 'k8yfdebo8kbbljxwuqjd1d253nuifv'
# Lista de canales a monitorear en Twitch
TWITCH_CHANNELS = ['aldimirco', 'baulo', 'florchus', 'chabon', 'illojuan', 'julianpz7', 'harryalexok', 'josedeodo', 'goncho', 'duendepablo', '0kempes', 'xqc', 'joaconeco', 'melianvalen', 'nanoide', 'youngmirko', 'nicolavorato', 's4vitaar', 'florchus777', 'athhe', 'lenar']
TWITCH_API_URL = "https://api.twitch.tv/helix/streams?user_login="

# Configuración de Kick
# Eliminamos la parte de la API oficial y usaremos scraping con Selenium.
# KICK_CHANNELS = ['baulo', 'melianvalen', 'nanoide', 'harryalexok', 'goncho', 'duendepablo', 'xqc', 'florenciafigola']

# Token del BOT para conectarse al chat (danteslto)
ACCESS_TOKEN = "z8u8bvalnndd8y1vlogpzjqqr26pbb"

# Función para obtener token de API (client_credentials) para Twitch
def get_twitch_api_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": "18ftiw25bcbp0h82df7267f8um88r1",  # Reemplaza con el Client Secret de tu aplicación
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params).json()
    return response.get("access_token")

TOKEN_API = get_twitch_api_token()

class Bot(commands.Bot):

    def __init__(self):
        # El bot se conecta al canal "daantesiito" (tu cuenta principal)
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=['daantesiito'])
        self.live_status = {channel: False for channel in TWITCH_CHANNELS}

    async def event_ready(self):
        print(f'Conectado como {self.nick}')  # Debería mostrar "danteslto"
        asyncio.create_task(self.check_channels_live())

    async def check_channels_live(self):
        while True:
            for channel in TWITCH_CHANNELS:
                live_status = is_twitch_live(channel)
                print(f"Twitch - {channel}: {live_status}")  # Debug
                await self.notify_if_live(channel, live_status, "Twitch")

            '''for channel in KICK_CHANNELS:
                live_status = is_kick_live(channel)
                print(f"Kick - {channel}: {live_status}")  # Debug
                await self.notify_if_live(channel, live_status, "Kick")'''

            await asyncio.sleep(60)  # Verifica cada 60 segundos

    async def notify_if_live(self, channel, live_status, platform):
        """Envía un mensaje en el chat si un streamer prende stream."""
        if live_status and not self.live_status[channel]:
            self.live_status[channel] = True
            notify_channel = self.get_channel('daantesiito')
            if not notify_channel and self.connected_channels:
                notify_channel = self.connected_channels[0]
            if notify_channel:
                print(f"Enviando notificación: {channel} en {platform}")
                await notify_channel.send(f"/me @daantesiito prendió {channel} en {platform}")
            else:
                print("No se encontró el canal para enviar el mensaje.")
        elif not live_status and self.live_status[channel]:
            self.live_status[channel] = False

    @commands.command(name='hola')
    async def hola(self, ctx):
        await ctx.send(f'¡Hola @{ctx.author.name}!')

def is_twitch_live(channel):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {TOKEN_API}'
    }
    response = requests.get(TWITCH_API_URL + channel, headers=headers)
    data = response.json()
    print(f"Data for Twitch channel {channel}: {data}")  # Debug
    return bool(data.get('data'))

'''def is_kick_live(username):
    """
    Verifica si un canal de Kick está en vivo mediante Selenium.
    Se basa en que, en la sección donde aparecen "nombre" y "seguidores",
    si el canal está en directo, el tercer elemento es un <div>,
    y si no, aparece un <span>[2] con "Última vez en vivo...".
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(f"https://kick.com/{username}")
        # Esperamos a que se cargue la zona esperada (hasta 10 segundos)
        wait = WebDriverWait(driver, 10)
        container = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[4]/main/div[2]/div[1]/div[1]/div[2]")))
        
        # Intentamos encontrar un <div> dentro de esa zona (indicativo de canal en directo)
        try:
            live_div = container.find_element(By.XPATH, "./div")
            driver.quit()
            return True
        except Exception:
            try:
                # Si no se encontró un div, buscamos el span que indica que no está en vivo
                offline_span = container.find_element(By.XPATH, "./span[2]")
                driver.quit()
                return False
            except Exception:
                driver.quit()
                return False
    except Exception as e:
        print(f"Error en Selenium para {username}: {e}")
        driver.quit()
        return False'''

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

if __name__ == "__main__":
    keep_alive()
    bot = Bot()
    bot.run()
