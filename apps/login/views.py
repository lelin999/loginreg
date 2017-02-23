from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

# Create your views here.
def index(req):
	if "poop" in req.session:
		redirect('/success')
	return render(req, 'login/index.html')

def regprocess(req):
	if req.method == 'GET':
		return redirect('/')
	if req.method == 'POST':
		if User.objects.validate(req.POST)[0]:
			name = req.POST['firstname']
			req.session['poop'] = name
			return redirect('/success')
		else:
			error_messages = User.objects.validate(req.POST)[1]
			for message in error_messages:
				messages.error(req, message)
			return redirect('/')

def loginprocess(req):
	if req.method == 'GET':
		return redirect('/')
	if req.method == 'POST':
		if User.objects.login(req.POST)[0]:
			name = User.objects.filter(email=req.POST['emaillogin'])[0].firstname
			req.session['poop'] = name
			return redirect('/success')
		else:
			error_messages = User.objects.login(req.POST)[1]
			for message in error_messages:
				messages.error(req, message)
			return redirect('/')

def success(req):
	context ={
		"users": User.objects.all()
	}
	if "poop" not in req.session:
		return redirect('/')
	else:	
		return render(req, 'login/success.html', context)

def logout(req):
	try:
		del req.session['poop']
	except KeyError:
		pass
	return redirect('/')

def reroute(req):
	return HttpResponse("invalid page")