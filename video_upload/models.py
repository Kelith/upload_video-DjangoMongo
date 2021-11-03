from djongo import models

class VideoMetadata(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    timestamp = models.DateTimeField()  
    duration_s = models.FloatField()
    bit_rate_kbps = models.IntegerField()
