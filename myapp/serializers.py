from rest_framework import serializers
from .models import Categories, Customers, Discounts, Inventoryadjustments, Items, Pricelists, Purchaseorders,AuthUser, Purchasereceipts, SalesorderDiscounts, Salesorders, Salesordertax, Shipments, StockItems, Stockmanagement, Taxconfigurations, Vendors, Warehouses

from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Get the original response data

        # Customize the response format
        return {
            "status": "success",
            "message": "Token refreshed successfully",
            "data": {
                "access_token": data["access"]
            }
        }

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class DiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discounts
        fields = '__all__'

class InventoryadjustmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventoryadjustments
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class PricelistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricelists
        fields = '__all__'

class PurchaseordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchaseorders
        fields = '__all__'

class PurchasereceiptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchasereceipts
        fields = '__all__'

class SalesorderDiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesorderDiscounts
        fields = '__all__'

class SalesordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesorders
        fields = '__all__'

class SalesordertaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesordertax
        fields = '__all__'

class ShipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = '__all__'

class StockItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItems
        fields = '__all__'

class StockmanagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stockmanagement
        fields = '__all__'

class TaxconfigurationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxconfigurations
        fields = '__all__'

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'

class VendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = '__all__'

class WarehousesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouses
        fields = '__all__'