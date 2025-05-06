from django import forms
from .models import customers, area, items, discounts

class ItemForm(forms.Form):
    item_id = forms.ModelChoiceField(queryset=items.objects.all(), label="Item")
    quantity = forms.IntegerField(min_value=1)
    discount_id = forms.ModelChoiceField(queryset=discounts.objects.filter(is_active=True), required=False)

class PlaceOrderForm(forms.Form):
    customer_id = forms.ModelChoiceField(queryset=customers.objects.all(), label="Customer")
    area_id = forms.ModelChoiceField(queryset=area.objects.all(), label="Delivery Area")
    
    # This will be a placeholder for multiple items, handled dynamically using JavaScript or extra logic
    # For now, simulate a basic field that captures order details as JSON-like string
    order_details = forms.CharField(widget=forms.HiddenInput())
