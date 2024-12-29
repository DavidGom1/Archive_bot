from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from config_data import config
import traceback, os, re

class Explorador:
#region --------------- variables de clase ---------------
    PASO_1, PASO_2, PASO_2_1, PASO_2_2, PASO_2_3, PASO_2_4, PASO_2_5, PASO_2_6, PASO_3, PASO_3_1 = range(10)
#endregion
#region --------------- metodo init -------------------
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
        self.asignatura_seleccionada = None
        self.mensajes_explorador = []
        self.mensajes_no_borrados = []
        self.local_path = os.path.join(os.getcwd(), config.local_path)
        self.actual_path = self.local_path
        self.opciones_basicas = [
                            [
                                InlineKeyboardButton("🔨 Crear carpeta", callback_data="crear_carpeta"),
                            InlineKeyboardButton("⬆️ Subir archivo", callback_data="subir_archivo")
                            ],
                            [
                            InlineKeyboardButton("🔙 Atrás", callback_data="atras"),
                            InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")
                            ]
                        ]
#endregion
#region --------------- metodos auxiliares ------------
    async def borrado_mensaje(self, mensajes):
        try:
            for mensaje in mensajes:
                if mensaje.message_id not in self.mensajes_no_borrados:
                    await mensaje.delete()
            self.mensajes_explorador = []
        except Exception as e:
            print(f'error en borrado_mensaje_receta {e}')
            pass

    def clean_char(self, char):
        car_esp = "!¡\"#$%&'()*+,-/:;<=>¿?@[\\]^`´{|}~ "
        letras_no_permitidas = "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
        cadena_limpia = re.sub(r'[{}]'.format(re.escape(car_esp + letras_no_permitidas)), '', char)
        return cadena_limpia

    async def cerrar_conversacion_explorador(self, context):
        #await self.borrado_mensaje_receta(mensaje_receta)
        mensajes = self.mensajes_explorador
        try:
            for mensaje in mensajes:
                await mensaje.delete()
            self.mensajes_explorador = []
            await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f"Conversación cerrada.")
            self.__init__()
        except Exception as e:
            print(f'error en cerrar_conversacion_explorador {e}')
        finally:
            print("Conversación cerrada con finally ejecutado")
            return ConversationHandler.END

    async def tiempo_espera(self, update, context):
        try:
            await self.borrado_mensaje(self.mensajes_explorador)
            self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f"Tiempo de espera superado, gracias {self.user} :)"))
            return ConversationHandler.END
        except Exception as e:
            print(f'error en tiempo_espera_receta {e}')

    #funcion que accede a la variable local_path de la clase Config y devuelve true si puede acceder a la ruta local
    def acceso_local(self):
        try:
            for asignatura in self.asignaturas:
                #comprueba si asignatura es una carpeta dentro de local_path, si no existe la crea, si existe pasas a la siguiente asignatura
                if not os.path.exists(f'{self.local_path}/{asignatura}'):
                    os.makedirs(f'{self.local_path}/{asignatura}')
            return True
        except Exception as e:
            print(f'error en acceso_local {e}')
            return False

    #funcion que retorna un array con las carpetas y archivos que hay en la ruta actual
    def explorar_directorio(self, path):
        try:
            #creo una lista de primero las carpetas y despues los archivos, ademas a las carpetas le pondre a la izquierda el icono de carpeta y a los archivos el icono de archivo
            contenido = []
            for item in os.listdir(path):
                if os.path.isdir(os.path.join(path, item)):
                    contenido.append(f"📁 {item}")
                else:
                    contenido.append(f"📄 {item}"
                    )
            return contenido
        except Exception as e:
            print(f'error en explorar_directorio {e}')
            return []

    async def funcion_retorno_contenido(self, context):
        try:
            #le quito la ultima carpeta del path actual
            self.actual_path = os.path.dirname(self.actual_path)
            contenido = self.explorar_directorio(self.actual_path)
            contenidos = []
            for item in contenido:
                    button = InlineKeyboardButton(item, callback_data=item.replace("📁 ", "").replace("📄 ", ""))
                    contenidos.append([button])
            if self.actual_path == self.local_path:
                contenidos.append([InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")])
                opciones = contenidos
                text = 'Selecciona la asignatura:'
            else:
                opciones = self.opciones_basicas
                opciones = contenidos + opciones
                text = '¿Qué quieres hacer?\nPulsa en una carpeta para acceder o en un archivo para mas opciones.'
            reply_markup = InlineKeyboardMarkup(opciones)
            # compruebo si dentro de la carpeta no hay archivos ni carpetas
            if len(os.listdir(self.actual_path)) == 0:
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='No hay nada en la carpeta.\n¿Qué quieres hacer?.', reply_markup=reply_markup))
            else:
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=text, reply_markup=reply_markup))
        except Exception as e:
            print(f'error en manejador_explorador {e}')
            traceback.print_exc()
            return ConversationHandler.END
#endregion
    async def iniciar_explorador(self, update, context):
        try:
            self.__init__()
            self.user = update.message.from_user.username
            self.chat_id = update.message.chat_id
            self.message_thread_id = update.message.message_thread_id
            self.acceso_local()
            opciones = []
            for asignatura in self.explorar_directorio(self.local_path):
                button = InlineKeyboardButton(asignatura, callback_data=asignatura.replace("📁 ", "").replace("📄 ", ""))
                opciones.append([button])
            opciones.append([InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")])
            reply_markup = InlineKeyboardMarkup(opciones)
            self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='Selecciona la asignatura:', reply_markup=reply_markup))
            return self.PASO_1
        except Exception as e:
            print(f'error en iniciar_explorador {e}')
            traceback.print_exc()
            return ConversationHandler.END

    async def manejador_explorador(self, update, context: CallbackQueryHandler):
        try:
            query = update.callback_query
            await query.answer()
        except Exception as e:
            print("si no hay query, hago esto")
            await self.funcion_retorno_contenido(context)
            return self.PASO_1
        try:
            await self.borrado_mensaje(self.mensajes_explorador)
            if query.data == "cerrar":
                mensajes = self.mensajes_explorador
                try:
                    for mensaje in mensajes:
                        await mensaje.delete()
                    self.mensajes_explorador = []
                    self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f"Conversación cerrada."))
                    # self.__init__()
                except Exception as e:
                    print(f'error en cerrar_conversacion_explorador {e}')
                finally:
                    return ConversationHandler.END
            elif query.data == "crear_carpeta":
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='¿Cómo se llamará la carpeta?'))
                return self.PASO_2
            elif query.data == "subir_archivo":
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='Envíame el archivo.'))
                return self.PASO_2_1
            elif query.data == "atras":
                print("atras")
                await self.funcion_retorno_contenido(context)
                return self.PASO_1
            elif query.data == "descargar":
                #muestro opciones para descargar al grupo o en privado
                opciones = [
                    [
                        InlineKeyboardButton("📤 Descargar en privado", callback_data="descargar_privado"),
                        InlineKeyboardButton("📤 Descargar en grupo", callback_data="descargar_grupo")
                    ],
                    [
                        InlineKeyboardButton("🔙 Atrás", callback_data="atras"),
                        InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(opciones)
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='Selecciona una opción:', reply_markup=reply_markup))
                return self.PASO_2_2
            elif query.data == "eliminar":
                opciones = [
                    [
                        InlineKeyboardButton("🗑️ Si, eliminar", callback_data="eliminar_confirmar"),
                        InlineKeyboardButton("No, cancelar", callback_data="volver"),
                    ],
                    [
                        InlineKeyboardButton("🔙 Atrás", callback_data="atras"),
                        InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(opciones)
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='¿Estás seguro de que quieres eliminar el archivo?', reply_markup=reply_markup))
                return self.PASO_2_2
            else:
                # compruebo si el query adquirido es una carpeta o un archivo
                self.actual_path = os.path.join(self.actual_path, query.data) #añado la carpeta seleccionada al path actual
                if not os.path.isfile(self.actual_path):
                    print("es una carpeta")
                else:
                    print("es un archivo")
                if not os.path.isfile(self.actual_path):
                    self.actual_path = self.actual_path.replace(query.data, "")
                    lista_de_contenido = self.explorar_directorio(self.actual_path.replace(query.data, "")) #obtengo el contenido de la carpeta seleccionada
                    for item in lista_de_contenido:
                            self.actual_path = os.path.join(self.actual_path, query.data) #añado la carpeta seleccionada al path actual
                            contenido = self.explorar_directorio(self.actual_path)
                            contenidos = []
                            for item in contenido:
                                    button = InlineKeyboardButton(item, callback_data=item.replace("📁 ", "").replace("📄 ", ""))
                                    contenidos.append([button])
                            opciones = self.opciones_basicas
                            # sumo ambas arrays
                            opciones = contenidos + opciones
                            reply_markup = InlineKeyboardMarkup(opciones)
                            # compruebo si dentro de la carpeta no hay archivos ni carpetas
                            if len(os.listdir(self.actual_path)) == 0:
                                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='No hay nada en la carpeta.\n¿Qué quieres hacer?.', reply_markup=reply_markup))
                            else:
                                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='¿Qué quieres hacer?\nPulsa en una carpeta para acceder o en un archivo para mas opciones.', reply_markup=reply_markup))
                            return self.PASO_1
                else:
                    # si es un archivo, muestro las opciones de descargar, eliminar y atras
                    opciones = [
                        [
                            InlineKeyboardButton("📥 Descargar", callback_data="descargar"),
                            InlineKeyboardButton("🗑️ Eliminar", callback_data="eliminar")
                        ],
                        [
                            InlineKeyboardButton("🔙 Atrás", callback_data="atras"),
                            InlineKeyboardButton("❌ Cerrar", callback_data="cerrar")
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(opciones)
                    self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='Selecciona una opción:', reply_markup=reply_markup))
                    return self.PASO_1
                
            # elif query.data == "crear_carpeta":
            #     self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='¿Cómo se llamará la carpeta?'))
            #     return self.PASO_2
            # else:
            #     self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f"Opción no válida."))
            #     self.cerrar_conversacion_explorador(context)
            #     return ConversationHandler.END
        except Exception as e:
            print(f'error en manejador_explorador {e}')
            traceback.print_exc()
            return ConversationHandler.END

    async def crear_carpeta(self, update, context):
        try:
            carpeta = update.message.text
            if not os.path.exists(f'{self.actual_path}/{carpeta}'):
                os.makedirs(f'{self.actual_path}/{carpeta}')
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f'Carpeta {carpeta} creada.'))
            else:
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f'La carpeta {carpeta} ya existe.'))
            # exploro las carpetas que hay en el directorio actual
            opciones = []
            for carpeta in self.explorar_directorio(self.actual_path):
                button = InlineKeyboardButton(carpeta, callback_data=carpeta.replace("📁 ", "").replace("📄 ", ""))
                opciones.append([button])
            opciones = opciones + self.opciones_basicas
            self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='Selecciona la carpeta:', reply_markup=InlineKeyboardMarkup(opciones)))
            return self.PASO_1
        except Exception as e:
            print(f'error en crear_carpeta {e}')
            traceback.print_exc()
            return ConversationHandler.END

    # creacion de la funcion subir archivo que lee el query de la asignatura seleccionada y ademas da opcion crear carpeta o subir archivo
    async def subir_archivo(self, update: Update, context):
        try:
            archivo = await update.message.effective_attachment.get_file()
            message = update.message
            doc = message.document
            nombre_archivo = self.clean_char(doc.file_name)
            try:
                await archivo.download_to_drive(os.path.join(self.actual_path, nombre_archivo))
            except Exception as e:
                print(f'error en subir_archivo {e}')
                traceback.print_exc()
                return ConversationHandler.END
            self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f'Archivo {doc.file_name} subido.'))
            opciones = []
            for carpeta in os.listdir(self.actual_path):
                button = InlineKeyboardButton(carpeta, callback_data=carpeta)
                opciones.append([button])
            opciones = opciones + self.opciones_basicas
            self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text='Selecciona la carpeta:', reply_markup=InlineKeyboardMarkup(opciones)))
            return self.PASO_1
        except Exception as e:
            print(f'error en subir_archivo {e}')
            traceback.print_exc()
            return ConversationHandler.END

    async def opciones_archivo(self, update, context):
        try:
            query = update.callback_query
            await query.answer()
            if query.data == "descargar_privado":
                #obtengo el id de la persona que ha solicitado la descarga
                user_id = query.from_user.id
                #envio el archivo en privado
                await context.bot.send_document(chat_id=user_id, document=open(self.actual_path, 'rb'))
                self.mensajes_explorador.append(await context.bot.send_message(chat_id=self.chat_id, message_thread_id = self.message_thread_id, text=f'Archivo enviado en privado.'))
                await self.funcion_retorno_contenido(context)
                return self.PASO_1
            elif query.data == "descargar_grupo":
                #envio el archivo en el grupo
                await self.borrado_mensaje(self.mensajes_explorador)
                await context.bot.send_document(chat_id=self.chat_id, document=open(self.actual_path, 'rb'))
                await self.funcion_retorno_contenido(context)
                return self.PASO_1
        except Exception as e:
            print("si no hay query, hago esto")
            return ConversationHandler.END

    def conversacion_explorador(self):
        return ConversationHandler(
            entry_points=[CommandHandler('archive', self.iniciar_explorador)],
            states={
                self.PASO_1: [CallbackQueryHandler(self.manejador_explorador)],
                self.PASO_2: [MessageHandler(filters.ALL, self.crear_carpeta)],
                self.PASO_2_1: [MessageHandler(filters.ALL, self.subir_archivo)],
                self.PASO_2_2: [CallbackQueryHandler(self.opciones_archivo)],
                    ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, self.tiempo_espera), CallbackQueryHandler(self.tiempo_espera)],
                },
                fallbacks=[CommandHandler('cerrar', self.cerrar_conversacion_explorador)],
                conversation_timeout=90,
            )