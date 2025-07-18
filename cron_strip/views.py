from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decouple import config
from cron_strip.utils import guardar_promedios_stripchat

@csrf_exempt
def ejecutar_cron(request):
    token = request.GET.get('token')
    if token != config('CRON_TOKEN'):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    # Acepta GET y POST
    if request.method in ['GET', 'POST']:
        try:
            guardar_promedios_stripchat()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
