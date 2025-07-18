from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cron_strip.utils import guardar_promedios_stripchat
from decouple import config

@csrf_exempt
def ejecutar_cron(request):
    token = request.GET.get('token')
    if token != config('CRON_TOKEN'):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        guardar_promedios_stripchat()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)