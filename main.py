from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import cfg.config as cfg #importamos el archivo de configuracion, donde se encuentra el token del bot y los administradores del mismo
import warnings, logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

warnings.filterwarnings('ignore')

if __name__ == '__main__':

    application = ApplicationBuilder().token(cfg.TOKEN).build()   #creamos la aplicacion

    # jobqueue = application.job_queue

    # recetas = Explorador().conversacion_explorador()
    # application.add_handler(recetas)  #agregamos el manejador de la conversacion

    # application.add_handler(CommandHandler('calendario', commands.calendario))  #agregamos el manejador del comando calendario

    # application.add_handler(CommandHandler('lista_compra', commands.lista_compra))  #agregamos el manejador del comando calendario

    # application.add_handler(CommandHandler('lista_compra_l_x_keep', commands.lista_compra_L_X_keep))  #agregamos el manejador del comando calendario

    # application.add_handler(CommandHandler('lista_compra_j_d_keep', commands.lista_compra_J_D_keep))  #agregamos el manejador del comando calendario

    # application.add_handler(CommandHandler('prueba', Calend.handle_gen_comidas_cenas))  #agregamos el manejador del comando ayuda

    # application.add_handler(MessageHandler(filters.TEXT, echo.echo))  #agregamos el manejador de mensajes de texto

    # jobqueue.run_repeating(Calend.gen_calend, interval=59)  # Intervalo de una semana (604800 segundos)

    application.run_polling()   #iniciamos la aplicacion
