from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BatteryStatus, CurrentData
from django.utils import timezone
from rest_framework import serializers

# Serializadores para los datos de la batería y corriente
class BatteryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatteryStatus
        fields = ['timestamp', 'voltage', 'percentage']

class CurrentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentData
        fields = ['timestamp', 'current_mA', 'remaining_time']

# Vista para recibir datos de sensores y almacenarlos
class SensorDataReceiver(APIView):
    def post(self, request):
        voltage = request.data.get("voltage")
        percentage = request.data.get("percentage")
        current_mA = request.data.get("current_mA")
        remaining_time = request.data.get("remaining_time")
        
        # Guardar datos en modelos correspondientes
        BatteryStatus.objects.create(voltage=voltage, percentage=percentage)
        CurrentData.objects.create(current_mA=current_mA, remaining_time=remaining_time)
        
        return Response({"message": "Datos guardados exitosamente"}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        # Opcional: manejar GET para verificar la disponibilidad del endpoint
        return Response({"message": "Endpoint disponible. Use POST para enviar datos."}, status=status.HTTP_200_OK)

# Vista para obtener datos de la batería
class BatteryDataReceiver(APIView):
    def get(self, request):
        # Obtener los últimos 100 datos de batería
        battery_data = BatteryStatus.objects.all().order_by('-timestamp')[:100]
        serializer = BatteryStatusSerializer(battery_data, many=True)
        return Response(serializer.data)

# Vista para obtener datos de corriente
class CurrentDataReceiver(APIView):
    def get(self, request):
        # Obtener los últimos 100 datos de corriente
        current_data = CurrentData.objects.all().order_by('-timestamp')[:100]
        serializer = CurrentDataSerializer(current_data, many=True)
        return Response(serializer.data)
