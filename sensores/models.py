from django.db import models

class BatteryStatus(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.DecimalField(decimal_places=2, max_digits=5)
    percentage = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.timestamp} - {self.voltage}V - {self.percentage}%"

class CurrentData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    current_mA = models.FloatField()
    remaining_time = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - {self.current_mA}mA - {self.remaining_time}hrs"
