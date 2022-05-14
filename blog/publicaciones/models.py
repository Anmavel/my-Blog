from django.db import models
from django.utils import timezone
from django.utils.html import format_html


# Arquitectura BD Relacional
# Objetivos:
#1. Evitar la redundancia de la información
#2. Buscar que el almacenamiento de la información sea óptimo

# tipos de Relaciones: (Una tabla es una entidad. Relaciones entre entidades)
# 1. Uno a uno (pareja)
# 2. Uno a muchos (un dato a muchos registros) (padre a hijos)
# 3. Muchos a Muchos (muchos datios a muchos registros)(Requiere una tabla auxiliar "Pivot Table" e intermediaria, que permite establecer el vínculo de una tabla a otra)

#Metodología para el diseno de la BD: Normalización
# 1FN: Toda tabla debe tener una llave primary (PK: primary key): identifoicador único de fila/registro
	# Primary key: atomicidad: valor != None/Null, valor no repetible
# 2FN: FK: Foreign Key: llave foránea/extranjera
# 3FN: 
# Create your models here.
class Post(models.Model):
	"""docstring for Post"""
	title = models.CharField(max_length=200)
	text= models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date= models.DateTimeField(blank=True, null=True)
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	imagen = models.FileField(upload_to='imagenes_blog/publicaciones/', blank=True, null=True) # capa del modelo va hasta aquí. Esta es la conexión con la base de datos

	def publish(self):
		self.published_date= timezone.now()
		self.save()

	def imagen_html(self):
		if self.imagen!= "" and self.imagen is not None:
			c_imagen='/'
		else:
			c_imagen=''
		return format_html('<img src="{}{}" style="height: 40px";/>', c_imagen, self.imagen)

	def __str__(self):
			return self.title
