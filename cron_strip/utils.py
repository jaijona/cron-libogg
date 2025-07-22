

import requests
from datetime import datetime
import pytz
from django.db import connection
from cron_strip.models import ModeloRegistrado,Promedio_strip,DataAllUseStrStrip

"""
def guardar_promedios_stripchat():
    try:
        studio_ids = ModeloRegistrado.objects.values_list('studio_id', flat=True).distinct()
        url = "https://es.stripchat.com/api/front/models"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://stripchat.com/"
        }

        colombia_tz = pytz.timezone("America/Bogota")
        ahora = datetime.now(colombia_tz)
        hora_actual = ahora.replace(minute=0, second=0, microsecond=0)

        limit = 99
        max_paginas = 50

        genero_a_primaryTag = {
            "Mujer": "girls",
            "Hombre": "men",
            "Trans": "trans",
            "Pareja": "couples"
        }

        for genero, primary_tag in genero_a_primaryTag.items():
            offset = 0
            posicion_global = 0
            encontrados = []

            total_modelos_api = 0
            total_usuarios_api = 0

            while offset < max_paginas * limit:
                params = {
                    "limit": limit,
                    "offset": offset,
                    "primaryTag": primary_tag,
                    "removeShows": "true"
                }

                response = requests.get(url, headers=headers, params=params)
                if response.status_code != 200:
                    print(f"❌ Error API Stripchat para género {genero}")
                    break

                data = response.json().get("models", [])
                if not data:
                    break

                for model in data:
                    posicion_global += 1
                    username = model.get("username")
                    viewers = model.get("viewersCount", 0)

                    if not username:
                        continue

                    total_modelos_api += 1
                    total_usuarios_api += viewers

                    encontrados.append({
                        "username": username.strip().lower(),
                        "posicion": posicion_global,
                        "usuarios": viewers
                    })

                offset += limit

            print(f"📊 Género: {genero}")
            print(f"   Total modelos en API: {total_modelos_api}")
            print(f"   Total usuarios conectados: {total_usuarios_api}")

            # Ahora, por cada estudio, si hay modelos registrados de este género, los procesamos
            for studio_id in studio_ids:
                modelos_db = ModeloRegistrado.objects.filter(
                    estado=1,
                    studio_id=studio_id,
                    genero__iexact=genero,
                    usuario_strip__isnull=False
                )

                usernames_deseados = {
                    m.usuario_strip.strip().lower(): m for m in modelos_db
                }

                for modelo_visible in encontrados:
                    username = modelo_visible["username"]
                    if username in usernames_deseados:
                        modelo_obj = usernames_deseados[username]

                        registro_existente = Promedio_strip.objects.filter(
                            id_modelo=modelo_obj,
                            id_studio=studio_id,
                            fecha=hora_actual
                        ).first()

                        if registro_existente:
                            nuevo_contador = registro_existente.contador + 1
                            nueva_posicion = (
                                (registro_existente.promedio * registro_existente.contador) +
                                modelo_visible["posicion"]
                            ) / nuevo_contador
                            nuevos_usuarios = (
                                (registro_existente.users * registro_existente.contador) +
                                modelo_visible["usuarios"]
                            ) / nuevo_contador

                            registro_existente.promedio = nueva_posicion
                            registro_existente.users = nuevos_usuarios
                            registro_existente.contador = nuevo_contador
                            registro_existente.save()
                        else:
                            Promedio_strip.objects.create(
                                id_modelo=modelo_obj,
                                id_studio=studio_id,
                                promedio=modelo_visible["posicion"],
                                users=modelo_visible["usuarios"],
                                fecha=hora_actual,
                                contador=1
                            )


        print("✅ Datos Stripchat guardados correctamente para todos los géneros.")

    except Exception as e:
        print("❗ Error guardando datos Stripchat:", e)

    finally:
        connection.close()

"""

def guardar_promedios_stripchat():
    try:
        studio_ids = ModeloRegistrado.objects.values_list('studio_id', flat=True).distinct()
        url = "https://es.stripchat.com/api/front/models"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://stripchat.com/"
        }

        colombia_tz = pytz.timezone("America/Bogota")
        ahora = datetime.now(colombia_tz)
        hora_actual = ahora.replace(minute=0, second=0, microsecond=0)

        limit = 99
        max_paginas = 80

        genero_a_primaryTag = {
            "Mujer": "girls",
            "Hombre": "men",
            "Trans": "trans",
            "Pareja": "couples"
        }

        resultados_por_genero = {
            "Mujer": {"modelos": 0, "usuarios": 0},
            "Hombre": {"modelos": 0, "usuarios": 0},
            "Trans": {"modelos": 0, "usuarios": 0},
            "Pareja": {"modelos": 0, "usuarios": 0},
        }

        for genero, primary_tag in genero_a_primaryTag.items():
            offset = 0
            posicion_global = 0
            encontrados = []

            total_modelos_api = 0
            total_usuarios_api = 0

            while offset < max_paginas * limit:
                params = {
                    "limit": limit,
                    "offset": offset,
                    "primaryTag": primary_tag,
                    "removeShows": "true"
                }

                response = requests.get(url, headers=headers, params=params)
                if response.status_code != 200:
                    print(f"❌ Error API Stripchat para género {genero}")
                    break

                data = response.json().get("models", [])
                if not data:
                    break

                for model in data:
                    posicion_global += 1
                    username = model.get("username")
                    viewers = model.get("viewersCount", 0)

                    if not username:
                        continue

                    total_modelos_api += 1
                    total_usuarios_api += viewers

                    encontrados.append({
                        "username": username.strip().lower(),
                        "posicion": posicion_global,
                        "usuarios": viewers
                    })

                offset += limit

            print(f"📊 Género: {genero}")
            print(f"   Total modelos en API: {total_modelos_api}")
            print(f"   Total usuarios conectados: {total_usuarios_api}")

            # Guardar los datos por género
            resultados_por_genero[genero]["modelos"] = total_modelos_api
            resultados_por_genero[genero]["usuarios"] = total_usuarios_api

            # Ahora, por cada estudio, si hay modelos registrados de este género, los procesamos
            for studio_id in studio_ids:
                modelos_registrados = ModeloRegistrado.objects.filter(
                    estado=1, studio_id=studio_id, genero=genero
                ).exclude(usuario_strip__isnull=True).exclude(usuario_strip__exact="")

                usernames_deseados = {
                    m.usuario_strip.strip().lower(): m for m in modelos_registrados
                }

                # Precargar registros existentes
                registros_existentes = Promedio_strip.objects.filter(
                    id_studio=studio_id,
                    fecha=hora_actual,
                    id_modelo__in=[m.id for m in modelos_registrados]
                )

                registros_dict = {
                    reg.id_modelo_id: reg for reg in registros_existentes
                }

                actualizados = []

                for modelo_visible in encontrados:
                    username = modelo_visible["username"]
                    if username in usernames_deseados:
                        modelo_obj = usernames_deseados[username]
                        registro_existente = registros_dict.get(modelo_obj.id)

                        if registro_existente:
                            nuevo_contador = registro_existente.contador + 1
                            registro_existente.promedio = (
                                (registro_existente.promedio * registro_existente.contador) +
                                modelo_visible["posicion"]
                            ) / nuevo_contador
                            registro_existente.users = (
                                (registro_existente.users * registro_existente.contador) +
                                modelo_visible["usuarios"]
                            ) / nuevo_contador
                            registro_existente.contador = nuevo_contador
                            actualizados.append(registro_existente)
                        else:
                            Promedio_strip.objects.create(
                                id_modelo=modelo_obj,
                                id_studio=studio_id,
                                promedio=modelo_visible["posicion"],
                                users=modelo_visible["usuarios"],
                                fecha=hora_actual,
                                contador=1
                            )

                if actualizados:
                    Promedio_strip.objects.bulk_update(
                        actualizados, ['promedio', 'users', 'contador']
                    )

        # Guardar en DataAllUseStrStrip
        total_modelos_all = sum([v["modelos"] for v in resultados_por_genero.values()])
        total_usuarios_all = sum([v["usuarios"] for v in resultados_por_genero.values()])

        registro_data, creado = DataAllUseStrStrip.objects.get_or_create(
            fecha=hora_actual,
            defaults={
                'strea_fem': resultados_por_genero["Mujer"]["modelos"],
                'users_fem': resultados_por_genero["Mujer"]["usuarios"],
                'strea_male': resultados_por_genero["Hombre"]["modelos"],
                'users_male': resultados_por_genero["Hombre"]["usuarios"],
                'strea_tra': resultados_por_genero["Trans"]["modelos"],
                'users_tra': resultados_por_genero["Trans"]["usuarios"],
                'strea_cou': resultados_por_genero["Pareja"]["modelos"],
                'users_cou': resultados_por_genero["Pareja"]["usuarios"],
                'strea_all': total_modelos_all,
                'users_all': total_usuarios_all,
                'contador': 1
            }
        )

        if not creado:
            c = registro_data.contador

            registro_data.strea_fem = (registro_data.strea_fem * c + resultados_por_genero["Mujer"]["modelos"]) / (c + 1)
            registro_data.users_fem = (registro_data.users_fem * c + resultados_por_genero["Mujer"]["usuarios"]) / (c + 1)
            registro_data.strea_male = (registro_data.strea_male * c + resultados_por_genero["Hombre"]["modelos"]) / (c + 1)
            registro_data.users_male = (registro_data.users_male * c + resultados_por_genero["Hombre"]["usuarios"]) / (c + 1)
            registro_data.strea_tra = (registro_data.strea_tra * c + resultados_por_genero["Trans"]["modelos"]) / (c + 1)
            registro_data.users_tra = (registro_data.users_tra * c + resultados_por_genero["Trans"]["usuarios"]) / (c + 1)
            registro_data.strea_cou = (registro_data.strea_cou * c + resultados_por_genero["Pareja"]["modelos"]) / (c + 1)
            registro_data.users_cou = (registro_data.users_cou * c + resultados_por_genero["Pareja"]["usuarios"]) / (c + 1)
            registro_data.strea_all = (registro_data.strea_all * c + total_modelos_all) / (c + 1)
            registro_data.users_all = (registro_data.users_all * c + total_usuarios_all) / (c + 1)
            registro_data.contador = c + 1

        registro_data.save()


        print("✅ Datos Stripchat guardados correctamente para todos los géneros.")

    except Exception as e:
        print("❗ Error guardando datos Stripchat:", e)

    finally:
        connection.close()
