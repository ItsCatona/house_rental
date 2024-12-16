from django import forms
from .models import Tenant, Property

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone', 'email', 'property', 'rent_due', 'move_in_date', 'move_out_date']


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'rent','image', 'area', 'beds', 'baths', 'garages']
