from datetime import date
from urllib import request
from django.core.paginator import Paginator
from django.db.models import Q

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render
from .models import Property, Tenant, Payment

from django.db.models import Sum  # For aggregating sums in queries
from datetime import datetime  # For working with dates

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

from .forms import TenantForm, PropertyForm


# Create your views here.
def base(request):
    return render(request, 'base.html')
def landlord_dashboard(request):
    properties = Property.objects.all()
    tenants = Tenant.objects.all()
    return render(request, 'landlord_dashboard.html', {'properties': properties, 'tenants': tenants})

def tenant_dashboard(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    return render(request, 'tenant_dashboard.html', {'tenant': tenant})

def starter_page(request):
    return render(request, 'starter-page.html')
def index(request):
    return render(request, 'index.html')
def agents(request):
    return render(request, 'agents.html')


def property_single(request):
    return render(request,'property-single.html')



def tenants_view(request):
    tenants = Tenant.objects.prefetch_related('payments').select_related('property').all()
    return render(request, 'tenants.html', {
        'tenants': tenants,
    })



def dashboard_view(request):
    current_year = datetime.now().year
    monthly_rent = []

    for month in range(1, 13):
        total = Payment.objects.filter(
            payment_date__year=current_year,
            payment_date__month=month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_rent.append(total)

    summary = {
        'total_properties': Property.objects.count(),
        'total_tenants': Tenant.objects.count(),
        'total_rent_due': Payment.objects.filter(status='due').aggregate(Sum('amount'))['amount__sum'] or 0,
        'paid_this_month': Payment.objects.filter(
            payment_date__month=datetime.now().month,
            payment_date__year=datetime.now().year,
        ).aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return render(request, 'dashboard.html', {
        'summary': summary,
        'recent_payments': Payment.objects.order_by('-payment_date')[:5],
        'recent_tenants': Tenant.objects.order_by('-move_in_date')[:5],
        'monthly_rent': monthly_rent,
    })




def properties_view(request):
    search_query = request.GET.get('search', '')
    filter_option = request.GET.get('filter', '')

    properties = Property.objects.all()

    # Search
    if search_query:
        properties = properties.filter(name__icontains=search_query)

    # Filter
    if filter_option == 'low-to-high':
        properties = properties.order_by('rent')
    elif filter_option == 'high-to-low':
        properties = properties.order_by('-rent')

    # Pagination
    paginator = Paginator(properties, 6)  # Show 6 properties per page
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)

    return render(request, 'properties.html', {'properties': properties, 'is_paginated': paginator.num_pages > 1})

def property_detail_view(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'property_detail.html', {'property': property})

def tenant_detail_view(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    return render(request, 'tenant_detail.html', {'tenant': tenant})



def contact_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Send an email (configure your email settings in settings.py)
        send_mail(
            f"Message from {name}",
            message,
            email,
            ['your_email@example.com'],  # Replace with your recipient email
        )

        messages.success(request, "Your message has been sent successfully!")
        return render(request, 'contact.html')

    return render(request, 'contact.html')



def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Log the user in
        login(request, user)
        messages.success(request, "Registration successful! Welcome to StaySync.")
        return redirect('dashboard')

    return render(request, 'register.html')



# Create Tenant
def create_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tenant added successfully!")
            return redirect('tenants')
    else:
        form = TenantForm()
    return render(request, 'create_tenant.html', {'form': form})

# Edit Tenant
def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, "Tenant updated successfully!")
            return redirect('tenants')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'edit_tenant.html', {'form': form})

# Delete Tenant
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        messages.success(request, "Tenant deleted successfully!")
        return redirect('tenants')
    return render(request, 'delete_tenant.html', {'tenant': tenant})

# Create Property
def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Property added successfully!")
            return redirect('properties')
    else:
        form = PropertyForm()
    return render(request, 'create_property.html', {'form': form})

# Edit Property
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully!")
            return redirect('properties')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'edit_property.html', {'form': form})

# Delete Property
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        property.delete()
        messages.success(request, "Property deleted successfully!")
        return redirect('properties')
    return render(request, 'delete_property.html', {'property': property})



def payments_view(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment_method = request.POST.get('payment_method')

        payment = get_object_or_404(Payment, id=payment_id)
        payment.payment_date = date.today()
        payment.payment_method = payment_method
        payment.status = 'paid'
        payment.save()
        return redirect('payments')  # Redirect to refresh the page

    payments = Payment.objects.select_related('tenant').all()
    return render(request, 'payments.html', {'payments': payments})


def first_payment(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)

    if request.method == 'POST':
        first_rent = request.POST.get('first_rent')
        deposit = request.POST.get('deposit')
        payment_method = request.POST.get('payment_method')

        # Record deposit payment
        if deposit:
            Payment.objects.create(
                tenant=tenant,
                month=date.today(),
                amount=deposit,
                payment_date=date.today(),
                payment_method=payment_method,
                status='paid',
                description='Deposit'
            )
            tenant.deposit_paid = True

        # Record first rent payment
        if first_rent:
            Payment.objects.create(
                tenant=tenant,
                month=date.today(),
                amount=first_rent,
                payment_date=date.today(),
                payment_method=payment_method,
                status='paid',
                description='First Rent'
            )

        tenant.save()
        return redirect('payments')  # Redirect to payments page

    return render(request, 'first_payment.html', {'tenant': tenant})


def move_out(request, tenant_id=None):
    if tenant_id is None:
        # Redirect to tenants list if no tenant_id is provided
        return redirect('tenants')

    tenant = get_object_or_404(Tenant, id=tenant_id)
    debts = tenant.calculate_debts()  # Calculate outstanding payments

    if request.method == 'POST':
        # Perform move-out actions
        tenant.move_out_date = date.today()
        tenant.property = None  # Free the property
        tenant.save()
        return redirect('tenants')  # Redirect to tenants list

    return render(request, 'move_out.html', {'tenant': tenant, 'debts': debts})






