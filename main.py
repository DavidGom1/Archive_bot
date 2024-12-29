from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from config_data import config #importamos el archivo de configuracion, donde se encuentra el token del bot y los administradores del mismo
from core import commands #importamos los archivos de las funciones que se ejecutaran en el bot
from core.archive import Explorador
import warnings, logging

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# warnings.filterwarnings('ignore')

if __name__ == '__main__':

    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler('start', commands.start))

    application.add_handler(CommandHandler('help', commands.help))

    recetas = Explorador().conversacion_explorador()
    application.add_handler(recetas)

    application.run_polling()   #iniciamos la aplicacion