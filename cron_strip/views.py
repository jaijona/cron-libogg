# views.py
"""
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decouple import config
from cron_strip.utils import guardar_promedios_stripchat

@csrf_exempt
def ejecutar_cron(request):
    token = request.GET.get('token') or request.POST.get('token')
    if token != config('CRON_TOKEN'):
        return JsonResponse({'error': 'Token inválido'}, status=403)

    try:
        guardar_promedios_stripchat()
        return JsonResponse({'status': 'OK'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

"""

from django.http import JsonResponse
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from cron_strip.utils import guardar_promedios_stripchat
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def ejecutar_cron(request):
    token = request.GET.get('token') or request.POST.get('token')

    logger.info("🔧 CRON endpoint fue llamado.")
    logger.info(f"Token recibido: {token}")

    if token != config('CRON_TOKEN'):
        logger.warning("❌ Token inválido.")
        return JsonResponse({'error': 'Token inválido'}, status=403)

    try:
        guardar_promedios_stripchat()
        logger.info("✅ Cron ejecutado correctamente.")
        return JsonResponse({'status': 'OK'})
    except Exception as e:
        logger.exception("💥 Error al ejecutar guardar_promedios_stripchat")
        return JsonResponse({'error': str(e)}, status=500)
