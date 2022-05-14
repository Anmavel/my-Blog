# Este es el módulo de la capa vista del proyecto
# también de ese componente http podemos importar otra función

# Modulo Vista del Proyecto
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# JSON: JavaScript Object Notation
from django.shortcuts import render
# Arquitectura MTV: Model Template View
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from publicaciones.models import Post
import datetime
from django.db.models import Q

#JSON: Javascript Object Notation
def home(request):
	#return HttpResponse("Hola Mundo desde la capa vista")
	#return HttpResponseRedirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ',request)
	context={}
	return render(request,'publicaciones/index.html',context)

@ensure_csrf_cookie
def blog(request):
	val_bus =''
	if request.method=="POST":

		if "buscar" in request.POST:

			val_bus=request.POST["buscar"];
			pub = Post.objects.filter(Q(title__contains=request.POST["buscar"]) | Q (text__contains=request.POST["buscar"]))
			#pub = Post.objects.filter(title__contains=request.POST["buscar"]).annotate(text__contains=request.POST["buscar"])
		else: 
			pub = Post.objects.all().order_by('-created_date')

	else:
		pub=Post.objects.all().order_by('-created_date')

	context={'publi':pub, 'filtro': 0, 'cant_items': pub.count(),'val_bus': val_bus}
	return render(request,'publicaciones/blog.html',context)


def blog_filtro(request, id_blog):
	val_bus=''
	pub= Post.objects.filter(id=id_blog)
	context={'publi':pub, 'filtro': 1, 'cant_items': pub.count(),'val_bus': val_bus}
	return render(request,'publicaciones/blog.html',context)

def site(request):
	context={}
	return render(request,'site/index-site.html',context)

@ensure_csrf_cookie
def login(request):
	context={}
	return render(request,'publicaciones/login.html',context)

def registrarse(request):
	context={}
	return render(request,'publicaciones/registrarse.html',context)

@ensure_csrf_cookie
def sign_in(request):
	if request.method=="POST":
		if "cuenta" in request.POST and "clave" in request.POST:
			#Realizamos la autentificación del usuario
			user= auth.authenticate(username=request.POST["cuenta"], password= request.POST["clave"])

			if user is not None:
				auth.login(request,user)
				usuario_id= user.id

				if request.session.session_key:
					id_session_new = request.session.session_key
				else:

					request.session = SessionStore()
					request.session["Miblog8867"]= datetime.datetime.now().timestamp()
					request.session.create()
					id_session_new = request.session.session_key

				return HttpResponseRedirect('/blog/', request)

			else: 

				context = {'error1': 'error en la cuenta o nombre de usuario'}
				return render(request,'publicaciones/login.html', context)

		else:
			context = {'error1':'Acceso no autorizado'}
			return render(request,'publicaciones/novalido.html', context)

	else:
		context = {'error1': '','mensaje': 'Bienvenido, cuidado con el DOG'}
		return render(request,'publicaciones/login.html', context)

@login_required(login_url='/blog/')
def logout(request):	
	auth.logout(request)
	return HttpResponseRedirect('/blog/login/',request)

@login_required(login_url='/blog/login/')
@ensure_csrf_cookie
def cambiar_clave(request):
	if request.user.is_authenticated:

		if request.method=="POST":

			if "clave_actual" in request.POST and "clave1" in request.POST and "clave2" in request.POST:

				if request.POST["clave1"]== request.POST["clave2"]:
					if request.user.check_password(request.POST["clave_actual"]):

						u = User.objects.get(pk=request.user.id)
						u.set_password(request.POST["clave1"])
						u.save()
						usuario=auth.authenticate(username=request.user,password=request.POST["clave1"])
						auth.login(request,usuario)
						context = {'error1': '','mensaje': 'Contraseña actualizada exitosamente','ch_pwd1': 1}
						return render(request,'publicaciones/change_password.html',context)

				else:
					context = {'error1': 'Error en confirmación de la contraseña!','mensaje': 'Actualizar mi Contraseña','ch_pwd1': 0}
					return render(request,'publicaciones/change_password.html',context)


			else:
				context = {'error1':'Acceso no autorizado'}
				return render(request,'publicaciones/novalido.html', context)

		else:
			context = {'error1': '', 'mensaje': 'Actualizar mi contraseña','ch_pwd1': 0}
			return render(request,'publicaciones/change_password.html',context)
	else:
		
		return HttpResponseRedirect('/blog/login/',request)

@login_required(login_url='/blog/login/')
@ensure_csrf_cookie
def mi_cuenta(request):

	if request.user.is_authenticated:

		if request.method=='POST':

			if "user_nm" in request.POST and "nombres" in request.POST and "apellidos" in request.POST and "email" in request.POST:

				u = User.objects.get(pk=request.user.id)
				u.username = request.POST["user_nm"]
				u.first_name = request.POST["nombres"]
				u.last_name = request.POST["apellidos"]
				u.email = request.POST["email"]
				u.save()
				context = {'error1': "Cuenta actualizada ok!" ,'ch_pwd1': 1, 'u_n':u}
				return render(request,'publicaciones/mi_cuenta.html',context)
			
			else:

				context = {"error1":"Acceso no autorizado!"}
				return render(request,'publicaciones/novalido.html',context)

		else:

			u = User.objects.get(pk=request.user.id) # ORM gegen SQL Injection
			context = {'error1': '', 'mensaje':'Mi Cuenta','ch_pwd1': 0, 'u_n': u}
			return render(request, 'publicaciones/mi_cuenta.html', context)
	else:
		
		return HttpResponseRedirect('/blog/login/',request)