from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context) -> None:
    await update.message.reply_text("¡Hola *" + update.message.from_user.username + "*!, soy el explorador de archivos en telegram para DAW del CarlosIII, desarrollado por la comunidad.\nSi tienes dudas consulta mi ayuda pulsando aqui --> /help\nTambién puedes pedir ayuda a un admin.\n¡Espero que te guste!", parse_mode='Markdown')

async def help(update: Update, context) -> None:
    await update.message.reply_text("¡TEXTO PARA LA AYUDA!", parse_mode='Markdown')