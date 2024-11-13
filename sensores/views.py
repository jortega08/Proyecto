from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import BatteryStatus, CurrentData
import json

@csrf_exempt
def receive_battery_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)  # Verifica qué datos estás recibiendo
            voltage = data.get('voltage')
            percentage = data.get('percentage')
            current_mA = data.get('current_mA')
            remaining_time = data.get('remaining_time')

            # Validar que los datos no sean None para evitar errores
            if voltage is not None and percentage is not None and current_mA is not None and remaining_time is not None:
                # Guardar los datos en la base de datos
                BatteryStatus.objects.create(voltage=voltage, percentage=percentage)
                CurrentData.objects.create(current_mA=current_mA, remaining_time=remaining_time)
                return JsonResponse({'status': 'success', 'message': 'Datos de batería y corriente recibidos correctamente'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Faltan algunos datos en la solicitud'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error al decodificar JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

led_states = {
    'led1': False,
    'led2': False,
    'led3': False,
    'led4': False
}

@csrf_exempt
def control_leds(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Actualiza los estados de los LEDs según los datos recibidos
        led_states['led1'] = data.get('led1', led_states['led1'])
        led_states['led2'] = data.get('led2', led_states['led2'])
        led_states['led3'] = data.get('led3', led_states['led3'])
        led_states['led4'] = data.get('led4', led_states['led4'])
        
        # Responde con el estado actualizado de los LEDs
        return JsonResponse(led_states, status=200)
    
    elif request.method == 'GET':
        # Devuelve el estado actual de los LEDs para solicitudes GET
        return JsonResponse(led_states, status=200)
    
    else:
        return JsonResponse({'error': 'Only POST and GET requests are allowed'}, status=405)
    
def led_control_page(request):
    return render(request, 'control_leds.html')

def battery_data_view(request):
    battery_data = BatteryStatus.objects.all().order_by('-timestamp')
    return render(request, 'battery_data.html', {'battery_data': battery_data})

def current_data_view(request):
    current_data = CurrentData.objects.all().order_by('-timestamp')
    return render(request, 'current_data.html', {'current_data': current_data})

def battery_status(request):
    # Obtener el último valor de la batería y de la corriente, si existen
    latest_battery_status = BatteryStatus.objects.latest('timestamp') if BatteryStatus.objects.exists() else None
    latest_current_data = CurrentData.objects.latest('timestamp') if CurrentData.objects.exists() else None
    
    # Obtener el porcentaje de la batería si existe un último valor de BatteryStatus
    battery_percentage = latest_battery_status.percentage if latest_battery_status else None

    return render(request, 'battery_status.html', {
        'battery_status': latest_battery_status,
        'current_data': latest_current_data,
        'battery_percentage': battery_percentage,
    })

