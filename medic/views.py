import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from medic.forms import UserForm, UserProfileForm, AnalysisForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Analysis, Ailment, User
from .helpers import *
from django.db.models import Count, Q

# Create your views here.

def index(request):
	return render(request, "index.html", {})

@login_required
def high_class_chart(request):
	dataset = Analysis.objects.values("user").annotate(hiv_count=Count('user', filter=Q(ailments=hiv)), ebola_count=Count('user', filter=Q(ailments=ebola)), cough_count=Count('user', filter=Q(ailments=cough)), tuberculosis_count=Count('user', filter=Q(ailments=tuberculosis)), malaria_count=Count('user', filter=Q(ailments=malaria))).order_by('user')
	
	categories = list()
	hiv_info = list()
	ebola_info = list()
	cough_info = list()
	tuberculosis_info = list()
	malaria_info = list()

	for entry in dataset:
		categories.append('User%s' % entry['user'])
		hiv_info.append(entry['hiv_count'])
		ebola_info.append(entry['ebola_count'])
		cough_info.append(entry['cough_count'])
		tuberculosis_info.append(entry['tuberculosis_count'])
		malaria_info.append(entry['malaria_count'])

	hiv_series = {
		'name': 'HIV Infected',
		'data': hiv_info,
		'color': 'green'
	}

	ebola_series = {
		'name': 'Ebola Infected',
		'data': ebola_info,
		'color': 'blue'
	}

	cough_series = {
		'name': 'Cough Infected',
		'data': cough_info,
		'color': 'red'
	}

	tuberculosis_series = {
		'name': "Tuberculosis Infected",
		'data': tuberculosis_info,
		'color': 'brown'
	}

	malaria_series = {
		'name': "Malaria Infected",
		'data': malaria_info,
		'color':'yellow'
	}

	chart = {
		'chart': {'type': 'column'},
		'title': {'text': 'Statistical Data of all Ailments'},
		'xAxis': {'categories': categories},
		'series': [hiv_series, ebola_series, cough_series, tuberculosis_series, malaria_series]
	}

	dump = json.dumps(chart)
	return render(request, 'ailment_chart.html', {'chart':dump})

@login_required
def display_data(request):
	analysis_info = Analysis.objects.all()
	# Calculate the ailment percentage for all ailments
	hiv_total = calculate_ailment_percentage(hiv_data, total_users)
	ebola_total = calculate_ailment_percentage(ebola_data, total_users)
	cough_total = calculate_ailment_percentage(cough_data, total_users)
	tuberculosis_total = calculate_ailment_percentage(tuberculosis_data, total_users)
	malaria_total = calculate_ailment_percentage(malaria_data, total_users)
	context = {"analysis_info":analysis_info, 'hiv_total':hiv_total, 'ebola_total':ebola_total, 'cough_total':cough_total, 'tuberculosis_total':tuberculosis_total, 'malaria_total':malaria_total}
	return render(request, 'analysis_data.html', context)

@login_required
def add_analysis(request):
	registered = False
	if request.method == "POST":
		analysis_form = AnalysisForm(data=request.POST)

		if analysis_form.is_valid():
			analysis = analysis_form.save(commit=False)
			analysis.user = request.user
			analysis.save()
			registered = True
	else:
		analysis_form = AnalysisForm()

	return render(request, 'add_medical_info.html', {'analysis_form':analysis_form, 'registered':registered})

def user_signup(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'signup.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your medic account has been disabled")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied")

	else:
		return render(request, 'login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))