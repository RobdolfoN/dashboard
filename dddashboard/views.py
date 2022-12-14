from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import CreateUserForm, CustomerForm, DataForm, CompanySizeform  #Orderform
# from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from .dataManagement import  handle_uploaded_file, sex_donut_industrychart, minority_donut_industrychart, aboriginal_donut_industrychart, disability_donut_industrychart, Companydata_sex_donut_industrychart, Companydata_minority_donut_industrychart, Companydata_aboriginal_donut_industrychart, Companydata_disability_donut_industrychart, sex_barchart_industrychart, minority_barchart_industrychart, aboriginal_barchart_industrychart, disability_barchart_industrychart, c_sex_barchart_industrychart, c_minority_barchart_industrychart, c_aboriginal_barchart_industrychart, c_disability_barchart_industrychart
import pathlib
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go





# Create your views here.

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Dashboard_user.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	#return render(request, 'accounts/register.html', context)
	return render(request, context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('industry')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'dddashboard/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Dashboard_user.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'dddashboard/dashboard.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def userPage(request):
# 	orders = request.user.customer.order_set.all()

# 	total_orders = orders.count()
# 	delivered = orders.filter(status='Delivered').count()
# 	pending = orders.filter(status='Pending').count()

# 	print('ORDERS:', orders)

# 	context = {'orders':orders, 'total_orders':total_orders,
# 	'delivered':delivered,'pending':pending}
# 	return render(request, 'dddashboard/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'dddashboard/account_settings.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'dddashboard/products.html', {'products':products})

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def customer(request, pk_test):
# 	customer = Dashboard_user.objects.get(id=pk_test)

# 	orders = customer.order_set.all()
# 	order_count = orders.count()

# 	myFilter = OrderFilter(request.GET, queryset=orders)
# 	orders = myFilter.qs 

# 	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
# 	'myFilter':myFilter}
# 	return render(request, 'dddashboard/customer.html',context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def createOrder(request, pk):
# 	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
# 	customer = Customer.objects.get(id=pk)
# 	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
# 	#form = OrderForm(initial={'customer':customer})
# 	if request.method == 'POST':
# 		#print('Printing POST:', request.POST)
# 		form = OrderForm(request.POST)
# 		formset = OrderFormSet(request.POST, instance=customer)
# 		if formset.is_valid():
# 			formset.save()
# 			return redirect('/')

# 	context = {'form':formset}
# 	return render(request, 'dddashboard/order_form.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	print('ORDER:', order)
	if request.method == 'POST':

		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'dddashboard/order_form.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def deleteOrder(request, pk):
# 	order = Order.objects.get(id=pk)
# 	if request.method == "POST":
# 		order.delete()
# 		return redirect('/')

# 	context = {'item':order}
# 	return render(request, 'dddashboard/delete.html', context)@login_required(login_url='login')

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def industry(request):
	dashboarduser = request.user
	print(dashboarduser)
	
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	print(dashboarduserinfo)
	dashboardusercompany = dashboarduserinfo.company_name
	print(dashboardusercompany)

	default = "all"
	filter = request.GET.get('filter', default)

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 24)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 24)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 24)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 24)

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 24)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 24)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 24)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 24)

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 24)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 24)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 24)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 24)

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 24)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 24)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 24)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 24)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 24)

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 24)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 24)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 24)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 24)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 24)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}
	if request.htmx:
		return render(request, 'dddashboard/industry.html', context)
	return render(request, 'dddashboard/industry.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def company(request):
	dashboarduser = request.user
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	dashboardusercompany = dashboarduserinfo.company_name

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 30)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 30)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 30)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 30)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 30)

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 30)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 30)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 30)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 30)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 30)

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 30)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 30)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 30)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 30)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 30)

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 30)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 30)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 30)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 30)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 30)

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 30)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 30)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 30)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 30)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany,30)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 30)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 30)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 30)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 30)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 30)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 30)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 30)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 30)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 30)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 30)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 30)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 30)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 30)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 30)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 30)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}
	# context = {}
	return render(request, 'dddashboard/company.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def historicalData(request):
	dashboarduser = request.user
	print(dashboarduser)
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	print(dashboarduserinfo)
	dashboardusercompany = dashboarduserinfo.company_name
	print(dashboardusercompany)

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive')
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader')
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent')
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson')
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor')

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive')
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader')
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent')
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson')
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor')

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive')
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader')
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent')
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson')
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor')

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive')
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader')
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent')
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson')
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor')

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}
	# context = {}
	return render(request, 'dddashboard/historical_data.html', context)







# def uploadFile(request):
# 	if request.method == 'POST':
# 		form = DataForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			name = form.cleaned_data.get('name')	
# 			handle_uploaded_file(request.FILES['file'])
# 			return redirect('/')
# 	else:
# 		form = DataForm()
# 	context = {'form':form}

# 	return render(request, 'dddashboard/upload.html', context)

# def uploadFile(request):
# 	if request.method == 'POST':
# 		form = DataForm(request.POST)
# 		# form.save()
# 		if form.is_valid():
# 			form.save()
# 		# return redirect('dddashboard/upload.html')	
		
# 	context = {'form':form}

# 	return render(request, 'dddashboard/upload.html', context)

def uploadFile(request):
	if request.method == 'POST':
		form = DataForm(request.POST, request.FILES)
		if form.is_valid():
			#company_name from forms is store in "form.cleaned_data['company_name']"
			#file uploaded from form is stored in "request.FILES" se puede consultar el nombre asi: print(request.FILES['file'])
			#se guarda nombre de compañia en variable
			name_of_company = form.cleaned_data['company_name'].lower()
			#borrar informacion de la tabla que contenga el nombre guardado en name_of_company
			#esto se hace para borrar la informacion del modelo CompanyData que esta relacionado con el nombre de la compañia que se acaba de crear
			CompanyName.objects.filter(name=name_of_company).delete()
			#se crea de nuevo una instancia en la tabla de los nombres.
			n, created = CompanyName.objects.get_or_create(name=name_of_company)

			uploaded_data = handle_uploaded_file(request.FILES['file'])

			for index, row in uploaded_data.iterrows():
				company_data = CompanyData.objects.create(
					name=n,
					gender_code=row["gender code"],
					aboriginal_peoples=row["aboriginal peoples"],
					visible_minorities=row["visible minorities"],
					person_with_disabilities=row["person with disabilities"],
					position_category=row["position/role category"],
					)
			return HttpResponse("The name of the uploaded file is " + form.cleaned_data['company_name'].lower())
	
	else:
		
		form = DataForm()

	return render(request, 'dddashboard/upload.html', {'form': form})


@admin_only
def admin_dashboard(request):
	if request.method == 'POST':
		form = DataForm(request.POST, request.FILES)
		if form.is_valid():
			#company_name from forms is store in "form.cleaned_data['company_name']"
			#file uploaded from form is stored in "request.FILES" se puede consultar el nombre asi: print(request.FILES['file'])
			#se guarda nombre de compañia en variable
			name_of_company = form.cleaned_data['company_name'].lower()
			size_of_company = form.cleaned_data['company_size'].lower()
			#borrar informacion de la tabla que contenga el nombre guardado en name_of_company
			#esto se hace para borrar la informacion del modelo CompanyData que esta relacionado con el nombre de la compañia que se acaba de crear
			CompanyName.objects.filter(name=name_of_company).delete()
			#se crea de nuevo una instancia en la tabla de los nombres.
			n, created = CompanyName.objects.get_or_create(name=name_of_company)
			s, created = CompanySize.objects.get_or_create(company_size=size_of_company)

			uploaded_data = handle_uploaded_file(request.FILES['file'])

			for index, row in uploaded_data.iterrows():
				company_data = CompanyData.objects.create(
					name=n,
					size=s, 
					gender_code=row["gender code"],
					aboriginal_peoples=row["aboriginal peoples"],
					visible_minorities=row["visible minorities"],
					person_with_disabilities=row["person with disabilities"],
					position_category=row["position/role category"],
					)
			messages.success(request, 'data uploaded for ' + form.cleaned_data['company_name'] + '!')
			return redirect('/admin')
	
	else:
		
		form = DataForm()

	return render(request, 'admin/admin_dashboard.html', {'form': form})

def navbarfooter(request):
	

	return render(request, 'dddashboard/dashboard_navbar_footer.html')

def demographicAboriginal(request):
	dashboarduser = request.user
	print(dashboarduser)
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	print(dashboarduserinfo)
	dashboardusercompany = dashboarduserinfo.company_name
	print(dashboardusercompany)

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 57)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 57)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 57)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 57)

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 57)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 57)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 57)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 57)

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 57)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 57)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 57)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 57)

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 57)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 57)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 57)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 57)

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}

	return render(request, 'dddashboard/demographic_variables/aboriginal.html', context)


def demographicDisability(request):
		
	dashboarduser = request.user
	print(dashboarduser)
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	print(dashboarduserinfo)
	dashboardusercompany = dashboarduserinfo.company_name
	print(dashboardusercompany)

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 57)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 57)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 57)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 57)

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 57)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 57)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 57)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 57)

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 57)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 57)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 57)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 57)

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 57)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 57)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 57)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 57)

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}

	

	return render(request, 'dddashboard/demographic_variables/persons_with_disabilities.html', context)


def demographicSex(request):

	dashboarduser = request.user
	print(dashboarduser)
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	print(dashboarduserinfo)
	dashboardusercompany = dashboarduserinfo.company_name
	print(dashboardusercompany)

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 57)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 57)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 57)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 57)

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 57)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 57)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 57)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 57)

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 57)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 57)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 57)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 57)

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 57)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 57)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 57)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 57)

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}

	

	return render(request, 'dddashboard/demographic_variables/sex.html', context)


def demographicMinority(request):
		
	dashboarduser = request.user
	print(dashboarduser)
	dashboarduserinfo = Dashboard_user.objects.get(name=dashboarduser)
	print(dashboarduserinfo)
	dashboardusercompany = dashboarduserinfo.company_name
	print(dashboardusercompany)

	#Industry data donut charts
	sex_dchart1, sexchart_hole_info =  sex_donut_industrychart()
	minority_dchart1, minority_hole_info =  minority_donut_industrychart()
	aboriginal_dchart1, aboriginal_hole_info =  aboriginal_donut_industrychart()
	disability_dchart1, disability_hole_info =  disability_donut_industrychart()

	#Company data donut charts
	Companydata_sex_dchart1, Companydata_sexchart_hole_info =  Companydata_sex_donut_industrychart(dashboardusercompany)
	Companydata_minority_dchart1, Companydata_minority_hole_info =  Companydata_minority_donut_industrychart(dashboardusercompany)
	Companydata_aboriginal_dchart1, Companydata_aboriginal_hole_info =  Companydata_aboriginal_donut_industrychart(dashboardusercompany)
	Companydata_disability_dchart1, Companydata_disability_hole_info =  Companydata_disability_donut_industrychart(dashboardusercompany)

# INDUSTRY DATA QUERIES
	#SEX DATA PER POSITION
	
	sex_executive_barchart = sex_barchart_industrychart('Executive', 57)
	sex_senior_leader_barchart = sex_barchart_industrychart('Senior Leader', 57)
	sex_manager_s_s_leader_barchart = sex_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	sex_foreperson_leader_barchart = sex_barchart_industrychart('Foreperson', 57)
	sex_individual_contributor_leader_barchart = sex_barchart_industrychart('Individual Contributor', 57)

	#VISIBLE MINORITY DATA PER POSITION
	minority_executive_barchart = minority_barchart_industrychart('Executive', 57)
	minority_senior_leader_barchart = minority_barchart_industrychart('Senior Leader', 57)
	minority_manager_s_s_leader_barchart = minority_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	minority_foreperson_leader_barchart = minority_barchart_industrychart('Foreperson', 57)
	minority_individual_contributor_leader_barchart = minority_barchart_industrychart('Individual Contributor', 57)

	#aboriginal DATA PER POSITION
	aboriginal_executive_barchart = aboriginal_barchart_industrychart('Executive', 57)
	aboriginal_senior_leader_barchart = aboriginal_barchart_industrychart('Senior Leader', 57)
	aboriginal_manager_s_s_leader_barchart = aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	aboriginal_foreperson_leader_barchart = aboriginal_barchart_industrychart('Foreperson', 57)
	aboriginal_individual_contributor_leader_barchart = aboriginal_barchart_industrychart('Individual Contributor', 57)

	#disabilities DATA PER POSITION
	disability_executive_barchart = disability_barchart_industrychart('Executive', 57)
	disability_senior_leader_barchart = disability_barchart_industrychart('Senior Leader', 57)
	disability_manager_s_s_leader_barchart = disability_barchart_industrychart('Manager/Supervisor/Superintendent', 57)
	disability_foreperson_leader_barchart = disability_barchart_industrychart('Foreperson', 57)
	disability_individual_contributor_leader_barchart = disability_barchart_industrychart('Individual Contributor', 57)

# Company DATA QUERIES
	#SEX DATA PER POSITION
	
	c_sex_executive_barchart = c_sex_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_sex_senior_leader_barchart = c_sex_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_sex_manager_s_s_leader_barchart = c_sex_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_sex_foreperson_leader_barchart = c_sex_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_sex_individual_contributor_leader_barchart = c_sex_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#VISIBLE MINORITY DATA PER POSITION
	c_minority_executive_barchart = c_minority_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_minority_senior_leader_barchart = c_minority_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_minority_manager_s_s_leader_barchart = c_minority_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_minority_foreperson_leader_barchart = c_minority_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_minority_individual_contributor_leader_barchart = c_minority_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#aboriginal DATA PER POSITION
	c_aboriginal_executive_barchart = c_aboriginal_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_aboriginal_senior_leader_barchart = c_aboriginal_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_aboriginal_manager_s_s_leader_barchart = c_aboriginal_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_aboriginal_foreperson_leader_barchart = c_aboriginal_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_aboriginal_individual_contributor_leader_barchart = c_aboriginal_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)

	#disabilities DATA PER POSITION
	c_disability_executive_barchart = c_disability_barchart_industrychart('Executive', dashboardusercompany, 57)
	c_disability_senior_leader_barchart = c_disability_barchart_industrychart('Senior Leader', dashboardusercompany, 57)
	c_disability_manager_s_s_leader_barchart = c_disability_barchart_industrychart('Manager/Supervisor/Superintendent', dashboardusercompany, 57)
	c_disability_foreperson_leader_barchart = c_disability_barchart_industrychart('Foreperson', dashboardusercompany, 57)
	c_disability_individual_contributor_leader_barchart = c_disability_barchart_industrychart('Individual Contributor', dashboardusercompany, 57)




	context = {'sex_dchart1': sex_dchart1, 'minority_dchart1':minority_dchart1, 'aboriginal_dchart1':aboriginal_dchart1, 'disability_dchart1':disability_dchart1, 'Companydata_sex_dchart1':Companydata_sex_dchart1, 'Companydata_minority_dchart1':Companydata_minority_dchart1, 'Companydata_aboriginal_dchart1':Companydata_aboriginal_dchart1, 'Companydata_disability_dchart1':Companydata_disability_dchart1,
		'sex_executive_barchart':sex_executive_barchart, 'sex_senior_leader_barchart':sex_senior_leader_barchart, 'sex_manager_s_s_leader_barchart':sex_manager_s_s_leader_barchart, 'sex_foreperson_leader_barchart':sex_foreperson_leader_barchart, 'sex_individual_contributor_leader_barchart':sex_individual_contributor_leader_barchart, 'minority_executive_barchart':minority_executive_barchart, 'minority_senior_leader_barchart':minority_senior_leader_barchart, 'minority_manager_s_s_leader_barchart':minority_manager_s_s_leader_barchart, 'minority_foreperson_leader_barchart':minority_foreperson_leader_barchart, 'minority_individual_contributor_leader_barchart':minority_individual_contributor_leader_barchart, 'aboriginal_executive_barchart':aboriginal_executive_barchart, 'aboriginal_senior_leader_barchart':aboriginal_senior_leader_barchart, 'aboriginal_manager_s_s_leader_barchart':aboriginal_manager_s_s_leader_barchart, 'aboriginal_foreperson_leader_barchart':aboriginal_foreperson_leader_barchart, 'aboriginal_individual_contributor_leader_barchart':aboriginal_individual_contributor_leader_barchart, 'disability_executive_barchart':disability_executive_barchart, 'disability_senior_leader_barchart':disability_senior_leader_barchart, 'disability_manager_s_s_leader_barchart':disability_manager_s_s_leader_barchart, 'disability_foreperson_leader_barchart':disability_foreperson_leader_barchart, 'disability_individual_contributor_leader_barchart':disability_individual_contributor_leader_barchart,
		'c_sex_executive_barchart':c_sex_executive_barchart, 'c_sex_senior_leader_barchart':c_sex_senior_leader_barchart, 'c_sex_manager_s_s_leader_barchart':c_sex_manager_s_s_leader_barchart, 'c_sex_foreperson_leader_barchart':c_sex_foreperson_leader_barchart, 'c_sex_individual_contributor_leader_barchart':c_sex_individual_contributor_leader_barchart, 'c_minority_executive_barchart':c_minority_executive_barchart, 'c_minority_senior_leader_barchart':c_minority_senior_leader_barchart, 'c_minority_manager_s_s_leader_barchart':c_minority_manager_s_s_leader_barchart, 'c_minority_foreperson_leader_barchart':c_minority_foreperson_leader_barchart, 'c_minority_individual_contributor_leader_barchart':c_minority_individual_contributor_leader_barchart, 'c_aboriginal_executive_barchart':c_aboriginal_executive_barchart, 'c_aboriginal_senior_leader_barchart':c_aboriginal_senior_leader_barchart, 'c_aboriginal_manager_s_s_leader_barchart':c_aboriginal_manager_s_s_leader_barchart, 'c_aboriginal_foreperson_leader_barchart':c_aboriginal_foreperson_leader_barchart, 'c_aboriginal_individual_contributor_leader_barchart':c_aboriginal_individual_contributor_leader_barchart, 'c_disability_executive_barchart':c_disability_executive_barchart, 'c_disability_senior_leader_barchart':c_disability_senior_leader_barchart, 'c_disability_manager_s_s_leader_barchart':c_disability_manager_s_s_leader_barchart, 'c_disability_foreperson_leader_barchart':c_disability_foreperson_leader_barchart, 'c_disability_individual_contributor_leader_barchart':c_disability_individual_contributor_leader_barchart,
		}

	

	return render(request, 'dddashboard/demographic_variables/visible_minority.html', context)
