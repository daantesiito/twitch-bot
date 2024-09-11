from twitchio.ext import commands

# Creamos el bot heredando de commands.Bot
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token='TU_TOKEN_DE_OAUTH', prefix='!', initial_channels=['tu_canal'])

    # Evento cuando el bot se conecta a Twitch
    async def event_ready(self):
        print(f'Conectado como {self.nick}')

    # Evento para manejar mensajes de chat
    async def event_message(self, message):
        # Imprimir el mensaje en la consola
        print(message.content)

        # Ignorar los mensajes del propio bot para evitar loops
        if message.author.name.lower() == self.nick.lower():
            return

        # Procesar los comandos si el mensaje tiene un prefijo válido
        await self.handle_commands(message)

    # Comando básico que responde con "Hola!" cuando escriben !saludo en el chat
    @commands.command(name='saludo')
    async def saludo(self, ctx):
        await ctx.send(f'¡Hola {ctx.author.name}!')

# Crear una instancia del bot
bot = Bot()

# Ejecutar el bot
bot.run()
