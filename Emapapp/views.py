from django.shortcuts import render
from .models import *
from .forms import *
from django.core.files import File
import re
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PIL import Image
from pathlib import Path
from django.http import HttpResponse
import smtplib
import random
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from django.utils import timezone

def index(request):
	lastdate = Celebr.objects.filter(can = "True")
	today = timezone.now()
	for i in lastdate:
		if i.date < today:
			Celebr.objects.filter(name = i.name, index = i.index).update(last = False)
	print(today)

	if request.method == 'POST':
		print(request.user.id)
		form = CForm(request.POST)
		logform = PostForm(request.POST)
		regform = RegForm(request.POST)
		if regform.is_valid():

			res = regform.save(commit=False)
			res.set_password(regform.cleaned_data['password'])
			res.save()

			usname = regform.cleaned_data.get('username', None)

			#a = Mybuh.objects.order_by('-mybuh')

			userid = User.objects.get(username = usname)
			userid = str(userid.id)
			with open('Emapapp/templates/Emapapp/mybuhs/mybuh'+userid+'.html', 'w', encoding="utf-8") as f:
				myfile = File(f)
				css = "css/profilecss.css"
				myfile.write(u'{% extends "Emapapp/base/basemybuh.html" %}{% load staticfiles %}{% block header %}{% endblock %}{% block maincontent %}{% endblock %}')
				myfile.closed
			f.closed
			with open('Emapapp/templates/Emapapp/profiles/profile'+userid+'.html', 'w', encoding="utf-8") as f:
				myfile = File(f)
				css = "css/profilecss.css"
				myfile.write(u'{% extends "Emapapp/base/baseprofile.html" %}{% load staticfiles %}{% block maincontent %}{% endblock %}')
				myfile.closed
			f.closed
			with open('Emapapp/templates/Emapapp/yetbuhs/yetbuh'+userid+'.html', 'w', encoding="utf-8") as f:
				myfile = File(f)
				css = "css/profilecss.css"
				myfile.write(u'{% extends "Emapapp/base/baseyetbuh.html" %}{% load staticfiles %}{% block header %}{% endblock %}{% block maincontent %}{% endblock %}')
				myfile.closed
			f.closed

			res1 = Mybuh(mybuh = userid)
			res1.user = User.objects.get(username = usname)
			res1.save()
			res4 = Yetbuh(yetbuh = userid)
			res4.user = User.objects.get(username = usname)
			res4.save()
			res3 = Reiting(reiting = '0', howmany = '0')
			res3.user = User.objects.get(username = usname)
			res3.save()
			res2 = Profile(profile = userid)
			res2.user = User.objects.get(username = usname)
			res2.save()
			res12 = avatar(image = 'standartuser.png')
			res12.user = User.objects.get(username = usname)
			res12.save()
			resmes = HaveMessages(havemes = False)
			resmes.user = User.objects.get(username = usname)
			resmes.save()

			login = regform.cleaned_data.get('username', None)
			password = regform.cleaned_data.get('password', None)

			user = auth.authenticate(username=login, password=password)
			print('Вход успешен')
			if user and user.is_active:
				auth.login(request, user)
		if logform.is_valid():
			login = logform.cleaned_data.get('login', None)
			password = logform.cleaned_data.get('password', None)
			user = auth.authenticate(username=login, password=password)
			print('Вход успешен')
			if user and user.is_active:
			    auth.login(request, user)
		if form.is_valid():
			a = Celebr.objects.order_by('-index')
			date = form.cleaned_data.get('date', None)
			date = re.split(r'\.', date)
			date = date[2] + '-' + date[1] + '-' + date[0]

			time = form.cleaned_data.get('time', None)
			time = time + ':00'
			date = date + ' ' + time
			print(date)
			if a.count():
				for b in a:
					lastfile = b.index
					break
				lastnum = int(lastfile)
				newnum = lastnum+1
			else:
				newnum = 0
			if(newnum<10):
				newfile = '00' + str(newnum)
			if(newnum>9):
				newfile = '0' + str(newnum)
			if(newnum>99):
				newfile = str(newnum)
			with open('Emapapp/templates/Emapapp/celebrs/ktoidet'+newfile+'.html', 'w', encoding="utf-8") as f:
				myfile = File(f)
				css = "css/profilecss.css"
				myfile.write(u'{% extends "Emapapp/base/basektoidet.html" %}{% load staticfiles %}{% block maincontent %}{% endblock %}')
				myfile.closed
			f.closed
			res = form.save(commit=False)
			res.index = newfile
			res.count = '0'
			res.last = True
			res.date = date
			res.maybecount = '0'
			res.can = True
			res.user = User.objects.get(id=request.user.id)
			res.save()
			return redirect("/")
	else:
		form = CForm()
	argv = {}
	argv['metka'] = Celebr.objects.all()
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
		print(argv['yetbuhmenu'])

		argv['tr'] = User.objects.get(id = request.user.id)
		b = Your.objects.filter(user = request.user.id)
		argv['your'] = str(b)
		b = MaybeYour.objects.filter(user = request.user.id)
		argv['maybeyour'] = str(b)
	return render(request, 'Emapapp/index.html', argv)

def profile(request, id):
	argv = {}
	b = Profile.objects.filter(user = request.user.id)
	if b.count() != 0 and str(b[0]) == str(id):
		argv['test'] = True
		argv['profile'] = Profile.objects.get(user = request.user.id)
		argv['coufriend'] = Friend.objects.filter(user = User.objects.get(id = request.user.id)).count()
		print('true')
	else:
		argv['test'] = False
		argv['pr'] = User.objects.get(id = id)
		argv['coufriend'] = Friend.objects.filter(user = User.objects.get(id = id)).count()

		if request.user.id != None:
			have = Friend.objects.filter(user = User.objects.get(id = request.user.id), friend=User.objects.get(id=id)).count()
			havem = MaybeFriend.objects.filter(user = User.objects.get(id=id), friend=User.objects.get(id = request.user.id)).count()
			haveyoum = MaybeFriend.objects.filter(user = User.objects.get(id = request.user.id), friend=User.objects.get(id=id)).count()
			print(have, havem)
			if have:
				argv['friend'] = True
			elif havem:
				argv['maybefriend'] = True
			elif haveyoum:
				argv['maybeyourfriend'] = True
			else:
				argv['friend'] = False
				argv['maybefriend'] = False
				argv['maybeyourfriend'] = False
			print('false')
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request, 'Emapapp/profiles/profile'+id+'.html', argv)

def change(request):
	if request.method == 'POST':
		form = ChaForm(request.POST)
		form1 = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			fn = form.cleaned_data.get('first_name', None)
			ln = form.cleaned_data.get('last_name', None)
			User.objects.filter(username=request.user.username).update(first_name=fn, last_name= ln)
			print("Изменения успешны")
		if form1.is_valid():
			image = form1.cleaned_data.get('image', None)
			avatar.objects.filter(user=request.user.id).delete()
			b = User.objects.get(username = request.user.username)
			res12 = avatar(image = image)
			res12.user = b
			res12.save()
			print("Изменения успешны")
			return redirect('/')
	else:
		form = ChaForm()
		form1 = ImageUploadForm()
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request, 'Emapapp/change.html', {'form': form, 'form1': form1})

def podpis(request, id):
	a = Celebr.objects.get(index = id)
	res1 = MaybeYour(yourcelebr = a.index)
	res1.user = User.objects.get(id= request.user.id)
	res1.save()

	newcount = Celebr.objects.get(index = id)
	print(newcount.maybecount)
	newcount = int(newcount.maybecount) + 1
	Celebr.objects.filter(index = id).update(maybecount = newcount)

	res = MaybeMembers(member = User.objects.get(id = request.user.id))
	res.cele = Celebr.objects.get(index = id)
	res.save()


	who = Celebr.objects.get(index = id)
	profilename = request.user.username
	mestype = 2
	ahref = "ktoidet" + id
	title = " подписался на ваше мероприятие " + Celebr.objects.get(index = id).name
	date = datetime.datetime.now()
	resmes = Messages(profilename = profilename, title = title, mestype = mestype, date = date, ahref = ahref)
	resmes.user = User.objects.get(id = who.user.id)
	resmes.save()

	HaveMessages.objects.filter(user = User.objects.get(id = who.user.id)).update(havemes = True)

	# newhowmany = Reiting.objects.get(user = User.objects.get(username = request.user.username))
	# print(newhowmany.howmany)
	# newhowmany = int(newhowmany.howmany) + 1
	# print(newhowmany)
	# Reiting.objects.filter(user = User.objects.get(username = request.user.username)).update(howmany = newhowmany)

	# b = Celebr.objects.all()

	# for i in b:
	# 	if(int(i.quantity) == int(i.count)):
	# 		print('hey')
	# 		f = Celebr.objects.filter(index = i.index).update(can = False)
	return redirect("/")

def otpis(request, id):
	havem = MaybeYour.objects.filter(yourcelebr = id, user = request.user.id).count()
	have = Your.objects.filter(yourcelebr = id, user = request.user.id).count()
	if havem == 1:
		MaybeYour.objects.get(yourcelebr = id, user = request.user.id).delete()
		MaybeMembers.objects.get(member = User.objects.get(id = request.user.id), cele = Celebr.objects.get(index = id)).delete()

		newcount = Celebr.objects.get(index = id)
		print(newcount.maybecount)
		newcount = int(newcount.maybecount) - 1
		Celebr.objects.filter(index = id).update(maybecount = newcount)
		print('hey')
	elif have == 1:
		Your.objects.get(yourcelebrinfo = Celebr.objects.get(index = id), user = request.user.id).delete()
		Members.objects.get(member = User.objects.get(id = request.user.id), cele = Celebr.objects.get(index = id)).delete()

		newcount = Celebr.objects.get(index = id)
		print(newcount.count)
		newcount = int(newcount.count) - 1
		Celebr.objects.filter(index = id).update(count = newcount)

		newhowmany = Reiting.objects.get(user = User.objects.get(id = request.user.id))
		print(newhowmany.howmany)
		newhowmany = int(newhowmany.howmany) - 1
		print(newhowmany)
		Reiting.objects.filter(user = User.objects.get(id = request.user.id)).update(howmany = newhowmany)

	# howmany = Reiting.objects.get(user = User.objects.get(username = request.user.username))
	# howmany = int(howmany.howmany) - 1
	# Reiting.objects.filter(user = User.objects.get(username = request.user.username)).update(howmany = howmany)

	# b = Celebr.objects.all()

	# for i in b:
	# 	if(int(i.quantity) > int(i.count)):
	# 		print('hey')
	# 		f = Celebr.objects.filter(index = i.index).update(can = True)

	print("Удалено")
	return redirect("/")

# def registration(request):
# 	if request.method == 'POST':
# 		form = RegForm(request.POST)
# 		if form.is_valid():

# 			res = form.save(commit=False)
# 			res.set_password(form.cleaned_data['password'])
# 			res.save()

# 			usname = form.cleaned_data.get('username', None)

# 			#a = Mybuh.objects.order_by('-mybuh')

# 			userid = User.objects.get(username = usname)
# 			userid = str(userid.id)
# 			with open('Emapapp/templates/Emapapp/mybuhs/mybuh'+userid+'.html', 'w', encoding="utf-8") as f:
# 				myfile = File(f)
# 				css = "css/profilecss.css"
# 				myfile.write(u'{% extends "Emapapp/mybuhs/mybuh0.html" %}{% load staticfiles %}{% block main %}{% endblock %}')
# 				myfile.closed
# 			f.closed
# 			with open('Emapapp/templates/Emapapp/profiles/profile'+userid+'.html', 'w', encoding="utf-8") as f:
# 				myfile = File(f)
# 				css = "css/profilecss.css"
# 				myfile.write(u'{% extends "Emapapp/base/baseprofile.html" %}{% load staticfiles %}{% block maincontent %}{% endblock %}')
# 				myfile.closed
# 			f.closed
# 			with open('Emapapp/templates/Emapapp/yetbuhs/yetbuh'+userid+'.html', 'w', encoding="utf-8") as f:
# 				myfile = File(f)
# 				css = "css/profilecss.css"
# 				myfile.write(u'{% extends "Emapapp/yetbuhs/yetbuh000.html" %}{% load staticfiles %}{% block main %}{% endblock %}')
# 				myfile.closed
# 			f.closed

# 			res1 = Mybuh(mybuh = userid)
# 			res1.user = User.objects.get(username = usname)
# 			res1.save()
# 			res4 = Yetbuh(yetbuh = userid)
# 			res4.user = User.objects.get(username = usname)
# 			res4.save()
# 			res3 = Reiting(reiting = '0', howmany = '0')
# 			res3.user = User.objects.get(username = usname)
# 			res3.save()
# 			res2 = Profile(profile = userid)
# 			res2.user = User.objects.get(username = usname)
# 			res2.save()
# 			res12 = avatar(image = 'standartuser.png')
# 			res12.user = User.objects.get(username = usname)
# 			res12.save()
# 			resmes = HaveMessages(havemes = False)
# 			resmes.user = User.objects.get(username = usname)
# 			resmes.save()

# 			login = form.cleaned_data.get('username', None)
# 			password = form.cleaned_data.get('password', None)

# 			user = auth.authenticate(username=login, password=password)
# 			print('Вход успешен')
# 			if user and user.is_active:
# 			    auth.login(request, user)

# 			# mail = User.objects.get(id = request.user.id)
# 			# mail = mail.email
# 			# to = mail # кому
# 			# gmail_user = 'myagkov_202@mail.ru' # от кого

# 			# smtpserver = smtplib.SMTP("smtp.mail.ru",587)

# 			# smtpserver.starttls() # шифрование по протоколу TLS
# 			# smtpserver.login(gmail_user, '123456qwertyuiop') # авторизуемся

# 			# header = 'Subject:Test message \n'
# 			# msg = header + str(a)
# 			# smtpserver.sendmail(gmail_user, to, msg)

# 			# smtpserver.close()
# 			# return redirect("/registration2")
# 			return redirect("/")
# 	else:
# 		form = RegForm()
# 	return render(request, 'Emapapp/registration.html', {'form': form})

# def registration2(request):
# 	random.seed
# 	a = int(random.uniform(0, 1000))
# 	print(a)

# 	mail = User.objects.get(id = request.user.id)
# 	mail = mail.email
# 	to = mail # кому
# 	gmail_user = 'myagkov_202@mail.ru' # от кого

# 	smtpserver = smtplib.SMTP("smtp.mail.ru",587)

# 	smtpserver.starttls() # шифрование по протоколу TLS
# 	smtpserver.login(gmail_user, '123456qwertyuiop') # авторизуемся

# 	header = 'Subject:Test message \n'
# 	msg = header + str(a)
# 	smtpserver.sendmail(gmail_user, to, msg)

# 	smtpserver.close()
# 	if request.method == 'POST':
# 		codeform = CodeForm(request.POST)
# 		if codeform.is_valid():
# 				code = codeform.cleaned_data.get('code', None)
# 				if code == str(a):
# 					print('ttt')
# 					return redirect("/")
# 				else:
# 					print("Неправильный код")
# 	else:
# 		codeform = CodeForm()
# 	return render(request, 'Emapapp/registration2.html', {'form': codeform})

def mybuh(request, id):
	argv = {}
	argv['info'] = Celebr.objects.filter(user = request.user.id)
	return render(request, 'Emapapp/mybuhs/mybuh'+id+'.html', argv)

def ktoidet(request, id):
	argv = {}
	argv['members'] = Members.objects.filter(cele = Celebr.objects.get(index = id))
	argv['maybemembers'] = MaybeMembers.objects.filter(cele = Celebr.objects.get(index = id))
	argv['cele'] = Celebr.objects.get(index = id)
	print(argv)
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request, 'Emapapp/celebrs/ktoidet'+id+'.html', argv)

def logout(request):
	auth.logout(request)
	print("Выход успешен")
	return redirect('/')

def login(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data.get('login', None)
			password = form.cleaned_data.get('password', None)
			user = auth.authenticate(username=login, password=password)
			print('Вход успешен')
			if user and user.is_active:
			    auth.login(request, user)
			    return redirect('/')
	else:
		form = PostForm()
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]

	return render(request, 'Emapapp/login.html', {'form':form})

def come(request, id):
	id = id.split('=')
	print(id)

	b = Reiting.objects.get(user=User.objects.get(id = id[0]))
	print(b.reiting)

	newreiting = (((int(b.reiting)/10) * (int(b.howmany)-1)) + 1) / int(b.howmany)
	print(newreiting)

	Reiting.objects.filter(user=User.objects.get(id = id[0])).update(reiting = int(newreiting*10))
	Members.objects.filter(cele=Celebr.objects.get(index = id[1]), member=User.objects.get(id = id[0])).update(ochenen = True)
	return redirect("/ktoidet"+id[1])

def notcome(request, id):
	id = id.split('=')
	print(id)

	b = Reiting.objects.get(user=User.objects.get(id = id[0]))
	print(b.reiting)

	newreiting = (((int(b.reiting)/10) * (int(b.howmany)-1)) + 0) / int(b.howmany)
	print(newreiting)

	Reiting.objects.filter(user=User.objects.get(id = id[0])).update(reiting = int(newreiting*10))
	Members.objects.filter(cele=Celebr.objects.get(index = id[1]), member=User.objects.get(id = id[0])).update(ochenen = True)
	return redirect("/ktoidet"+id[1])

def agree(request, id):
	id = id.split('=')
	print(id)

	a = Celebr.objects.get(index = id[1])

	MaybeMembers.objects.get(member = User.objects.get(id = id[0]), cele = Celebr.objects.get(index = id[1])).delete()
	MaybeYour.objects.get(user = User.objects.get(id = id[0]), yourcelebr = id[1]).delete()
	Celebr.objects.filter(index = id[1]).update(maybecount = int(a.maybecount) - 1)

	res1 = Your(yourcelebr = a.index, yourcelebrinfo = a)
	res1.user = User.objects.get(id= id[0])
	res1.save()

	newcount = Celebr.objects.get(index = id[1])
	print(newcount.count)
	newcount = int(newcount.count) + 1
	Celebr.objects.filter(index = id[1]).update(count = newcount)

	res = Members(member = User.objects.get(id = id[0]), ochenen = False)
	res.cele = Celebr.objects.get(index = id[1])
	res.save()

	newhowmany = Reiting.objects.get(user = User.objects.get(id = id[0]))
	print(newhowmany.howmany)
	newhowmany = int(newhowmany.howmany) + 1
	print(newhowmany)
	Reiting.objects.filter(user = User.objects.get(id = id[0])).update(howmany = newhowmany)

	b = Celebr.objects.all()

	for i in b:
		if(int(i.quantity) == int(i.count)):
			print('hey')
			f = Celebr.objects.filter(index = i.index).update(can = False)

	return redirect("/ktoidet"+id[1])

def notagree(request, id):
	id = id.split('=')
	print(id)

	a = Celebr.objects.get(index = id[1])

	MaybeMembers.objects.get(member = User.objects.get(id = id[0]), cele = Celebr.objects.get(index = id[1])).delete()
	MaybeYour.objects.get(user = User.objects.get(id = id[0]), yourcelebr = id[1]).delete()
	Celebr.objects.filter(index = id[1]).update(maybecount = int(a.maybecount) - 1)

	return redirect("/ktoidet"+id[1])

def yetbuh(request, id):
	argv = {}
	argv['info'] = Members.objects.filter(member = User.objects.get(id = request.user.id))
	argv['favo'] = Favourites.objects.filter(user = User.objects.get(id = request.user.id))
	argv['favo'] = str(argv['favo'])
	for i in argv['info']:
		print(i.cele.user.id,"|",argv['favo'])
		i.cele.user.id = str(i.cele.user.id)
		if i.cele.user.id in argv['favo']:
			print('have')
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request, 'Emapapp/yetbuhs/yetbuh'+id+'.html', argv)

#@csrf_exempt - если че отменяет проверку csrf
def favourite(request, id):
	if request.method == 'POST':
		b = Favourites.objects.filter(favourite = User.objects.get(id = id).id, user = User.objects.get(id = request.user.id)).count()
		print(b)
		if b == 1:
			Favourites.objects.get(favourite = User.objects.get(id = id).id, user = User.objects.get(id = request.user.id)).delete()
			print('yes')
		else:
			print('no')
			res = Favourites(favourite = User.objects.get(id = id).id)
			res.user = User.objects.get(id = request.user.id)
			res.save()
		print('ok')
		return HttpResponse('Ok', content_type='text/html')
	else:
		print('hel')
		return HttpResponse('Error', content_type='text/html')

def users(request):
	users = {}
	argv = {}
	if request.method == 'POST':
		allusers = User.objects.all()
		userform = UseForm(request.POST)
		if userform.is_valid():
			thatuser = userform.cleaned_data.get('user', None)
			a = 0
			for i in allusers:
				print(thatuser,"|",i)
				result = re.search(str(thatuser), str(i))
				if result != None:
					us = User.objects.get(username = i)
					users[us] = a
					a = a + 1
			argv['users'] = users
		else:
			argv['users'] = User.objects.all()
	else:
		argv['users'] = User.objects.all()
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request, 'Emapapp/userssearch.html', argv)


def addfriend(request,id):
	have = Friend.objects.filter(user = User.objects.get(id = request.user.id), friend=User.objects.get(id = id)).count()
	havem = MaybeFriend.objects.filter(user = User.objects.get(id = id), friend=User.objects.get(id = request.user.id)).count()
	print('count: ',have)
	if have == 0 and havem == 0:
		res2 = MaybeFriend(friend = User.objects.get(id = request.user.id))
		res2.user = User.objects.get(id = id)
		res2.save()
		print('add')
	if have == 1:
		Friend.objects.get(user = User.objects.get(id = request.user.id), friend=User.objects.get(id = id)).delete()
		Friend.objects.get(user = User.objects.get(id = id), friend=User.objects.get(id = request.user.id)).delete()
		print('delete')
	if havem == 1:
		MaybeFriend.objects.get(user = User.objects.get(id = id), friend=User.objects.get(id = request.user.id)).delete()
		print('delete')
	return redirect("/profile"+id)

def messages(request, id):
	mes = Messages.objects.filter(user = User.objects.get(id = id))
	argv = {}
	argv['mes'] = mes
	HaveMessages.objects.filter(user = User.objects.get(id = id)).update(havemes = False)
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request, "Emapapp/messages.html", argv)

def friends(request, id):
	argv = {}
	users = {}
	if str(request.user.id) == str(id):
		argv['id'] = True
	else:
		argv['id'] = False
	if request.method == 'POST':
		allfriends = Friend.objects.filter(user = User.objects.get(id = id))
		userform = UseForm(request.POST)
		if userform.is_valid():
			thatuser = userform.cleaned_data.get('user', None)
			a = 0
			for i in allfriends:
				print(thatuser,"|",i.friend.username)
				result = re.search(str(thatuser), str(i.friend.username))
				if result != None:
					us = Friend.objects.get(user = request.user, friend = i.friend)
					users[us] = a
					a = a + 1
			argv['friend'] = users
	else:		
		argv['friend'] = Friend.objects.filter(user = User.objects.get(id = id))
		argv['maybefriend'] = MaybeFriend.objects.filter(user = User.objects.get(id = id))
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request, "Emapapp/friends.html", argv)

def add(request, id):

	MaybeFriend.objects.get(user = User.objects.get(id = request.user.id), friend=User.objects.get(id = id)).delete()

	res = Friend(friend = User.objects.get(id = id))
	res.user = User.objects.get(id = request.user.id)
	res.save()
	res2 = Friend(friend = User.objects.get(id = request.user.id))
	res2.user = User.objects.get(id = id)
	res2.save()

	return redirect("/friends"+str(request.user.id))

def notadd(request, id):

	MaybeFriend.objects.get(user = User.objects.get(id = id), friend=User.objects.get(id = request.user.id)).delete()

	return redirect("/friends"+str(request.user.id))


def form(request):
	argv = {}
	argv['mes'] = OnlineMes.objects.filter(user=User.objects.get(id = request.user.id), to = User.objects.get(username = "Alex228"))
	print(argv['mes'])
	return render(request, "Emapapp/form.html", argv)

def messageonline(request):
	if request.method == "POST":
		text = request.POST.get('the_post')

		count = OnlineMes.objects.filter(user=User.objects.get(id = request.user.id), to = User.objects.get(username = "Alex228")).count()
		print(text, count)
		if count != 0:
			mes = OnlineMes.objects.filter(user=User.objects.get(id = request.user.id), to = User.objects.get(username = "Alex228")).order_by('-message_id')
			for i in mes:
				print(i.message_id)
				newid = int(i.message_id) + 1
				print(newid)
				break;
		else:
			newid = 0;

		res = OnlineMes(message = text, to=User.objects.get(username="Alex228"), readed = 'False', message_id= newid)
		res.user = User.objects.get(id = request.user.id)
		res.save()


	if request.method == "GET":
		print(request.GET['count'])
		if str(request.GET['count']) == 'True':
			print(str(request.GET['to']))
			mes = OnlineMes.objects.filter(user=User.objects.get(id = request.user.id), to = User.objects.get(username = str(request.GET['to'])), readed = 'False')
			count = mes.count()
			print(count)
			return HttpResponse(count)
		else:
			print('else')
			print(str(request.GET['to']))
			mes = OnlineMes.objects.filter(user=User.objects.get(id = request.user.id), to = User.objects.get(username = str(request.GET['to'])), readed = 'False').reverse()
			print(mes)
			data = ''
			for i in mes:
				data = i.message
				OnlineMes.objects.filter(user=User.objects.get(id = request.user.id), to = User.objects.get(username = str(request.GET['to'])), readed = 'False', message_id=i.message_id).update(readed = "True")
				break
			print(data)
			return HttpResponse(data)
	return redirect("/form")


def calendar(request):
	argv = {}
	argv['date'] = Celebr.objects.all();
	argv['count'] = Celebr.objects.filter(last = 'True', can = 'True').count()
	if request.user.is_authenticated:
		argv['yetbuhmenu'] = Your.objects.order_by('date').filter(user = request.user)[:8]
		argv['mybuhmenu'] = Celebr.objects.order_by('date').filter(user = request.user)[:8]
		argv['mes'] = Messages.objects.order_by('date').filter(user = request.user)[:8]
	return render(request,"Emapapp/calendar.html", argv)