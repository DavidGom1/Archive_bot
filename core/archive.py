from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import traceback

class Explorador:
    PASO_1, PASO_2, PASO_2_1, PASO_2_2, PASO_2_3, PASO_2_4, PASO_2_5, PASO_2_6, PASO_3, PASO_3_1 = range(10)

    def __init__(self):
        self.chat_id = None
        self.message_thread_id = None
        self.user = None
        self.asignaturas = [
            "Programación",
            "Bases de Datos",
            "Entornos de Desarrollo",
            "Lenguaje de Marcas",
            "Sistemas Informaticos",
            "IPE",
            "Inglés",
            "Digitalización"
        ]
        self.mensajes_explorador = []
        self.mensajes_no_borrados = []

    async def borrado_mensaje(self, mensajes):
        try:
            for mensaje in mensajes:
                if mensaje.message_id not in self.mensajes_no_borrados:
                    await mensaje.delete()
            self.mensajes_explorador = []
        except Exception as e:
            print(f'error en borrado_mensaje_receta {e}')
            pass

    async def cerrar_conversacion_receta(self, context):
        #await self.borrado_mensaje_receta(mensaje_receta)
        mensajes = self.mensajes_explorador
        try:
            for mensaje in mensajes:
                await mensaje.delete()
            self.mensajes_explorador = []
            await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f"Conversación cerrada.")
            self.__init__()
        except Exception as e:
            print(f'error en cerrar_conversacion_receta {e}')
        finally:
            print("Conversación cerrada con finally ejecutado")
            return ConversationHandler.END

    async def tiempo_espera(self, update, context):
        try:
            await self.borrado_mensaje(self.mensajes_explorador)
            self.mensaje_receta.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f"Tiempo de espera superado, gracias {self.user} :)"))
            return ConversationHandler.END
        except Exception as e:
            print(f'error en tiempo_espera_receta {e}')

    async def iniciar_explorador(self, update, context):
        try:
            self.user = update.message.from_user.username
            self.chat_id = update.message.chat_id
            self.message_thread_id = update.message.message_thread_id
            opciones = []
            for asignatura in self.asignaturas:
                opciones.append([InlineKeyboardButton(asignatura, callback_data=asignatura)])
            reply_markup = InlineKeyboardMarkup(opciones)
            self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='¿Qué archivo deseas explorar?', reply_markup=reply_markup))
            return self.PASO_1
        except Exception as e:
            print(f'error en iniciar_explorador {e}')
            traceback.print_exc()
            return ConversationHandler.END

    async def explorar(self, update, context):
        self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='Explorando...'))
        return ConversationHandler.END

    def conversacion_explorador(self):
        return ConversationHandler(
            entry_points=[CommandHandler('archive', self.iniciar_explorador)],
            states={
                self.PASO_1: [CallbackQueryHandler(self.explorar)],
                    ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, self.tiempo_espera), CallbackQueryHandler(self.tiempo_espera)],
                },
                fallbacks=[CommandHandler('cerrar', self.cerrar_conversacion_receta)],
                conversation_timeout=90,
            )