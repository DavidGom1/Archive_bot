from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context) -> None:
    await update.message.reply_text("¡Hola *" + update.message.from_user.username + "*!, soy el explorador de archivos en telegram para DAW del CarlosIII, desarrollado por la comunidad.\nSi tienes dudas consulta mi ayuda pulsando aqui --> /help\nTambién puedes pedir ayuda a un admin.\n¡Espero que te guste!", parse_mode='Markdown')

async def help(update: Update, context) -> None:
    await update.message.reply_text("¡Bienvenido a Archive Bot\nUn bot sencillo para ayudarte a gestionar y organizar tus archivos.\n\nComandos disponibles:\n\n/start - Inicia el bot y muestra un mensaje de bienvenida.\n/help - Muestra esta lista de comandos y su descripción.\n/archive - Guarda un archivo o mensaje importante en tu archivo personal.\n💡 Consejos:\n\nUsa /archive para almacenar mensajes o archivos importantes.\nSi tienes dudas, utiliza /help para obtener información sobre cómo usar el bot.\n¡Gracias por usar Archive Bot! 😊!", parse_mode='Markdown')