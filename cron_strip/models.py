from django.db import models
from django.utils import timezone

class InfoStudio(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)  # Suponiendo que está guardada como texto plano
    cargo = models.CharField(max_length=150)
    id_studio = models.IntegerField()
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'info_users'  # 👈 Esto conecta directamente con tu tabla existente
        managed = False  # 👈 Le decimos a Django que NO debe crear ni modificar esta tabla

class ModeloRegistrado(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    jornada = models.CharField(max_length=50)
    genero = models.CharField(max_length=50)
    fecha = models.DateField(default=timezone.now)
    estado = models.IntegerField(default=1)
    id_monitor = models.IntegerField(default=0)
    usuario_strip = models.CharField(max_length=100,default=0)
    studio= models.ForeignKey(InfoStudio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'data_models'
        constraints = [
            models.UniqueConstraint(fields=['studio', 'usuario','usuario_strip'], name='unique_usuario_por_studio')
        ]
        #ordering = ['-fecha_registro']

    def __str__(self):
        #return self.nombre,self.usuario
        return f"{self.nombre} ({self.usuario})"
    

class Promedio_strip(models.Model):
    id = models.AutoField(primary_key=True)
    #id_modelo = models.IntegerField()
    id_modelo = models.ForeignKey(ModeloRegistrado, db_column='id_modelo', on_delete=models.CASCADE)
    id_studio = models.IntegerField()
    promedio = models.FloatField()
    contador = models.IntegerField()
    users = models.IntegerField(default=0)
    fecha = models.DateTimeField()

    class Meta:
        managed = False  # <-- IMPORTANTE: Django no modificará esta tabla
        db_table = 'promedio_strip'


class DataAllUseStrStrip(models.Model):
    fecha = models.DateTimeField()
    strea_all = models.IntegerField(default=0)
    strea_fem = models.IntegerField(default=0)
    strea_male = models.IntegerField(default=0)
    strea_tra = models.IntegerField(default=0)
    strea_cou = models.IntegerField(default=0)
    
    users_all = models.FloatField(default=0)
    users_fem = models.FloatField(default=0)
    users_male = models.FloatField(default=0)
    users_tra = models.FloatField(default=0)
    users_cou = models.FloatField(default=0)

    contador = models.IntegerField(default=0)
    class Meta:
        db_table = 'data_all_use_str_strip'  # nombre personalizado opcional
        managed = False  