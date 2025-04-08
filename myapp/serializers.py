from rest_framework import serializers
from .models import Categories, salesorder_return, PurchaseOrder_return,salesorder_returndetail, Customers, Discounts,SalesOrderDetail, Area, Inventoryadjustments, Items,  Purchaseorders,User, Purchasereceipts, SalesorderDiscounts, Salesorders, Salesordertax, Shipments, StockItems, Stockmanagement, Taxconfigurations, Vendors, Warehouses

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
        
class PurchaseOrder_returnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder_return
        fields = '__all__'

class salesorder_returnSerializer(serializers.ModelSerializer):
    class Meta:
        model = salesorder_return
        fields = '__all__'

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

# class SalesordersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Salesorders
#         fields = '__all__'

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

class salesorder_returndetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stockmanagement
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
        model = User
        fields = '__all__'

class VendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = '__all__'

class WarehousesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouses
        fields = '__all__'
        
        
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'
        
# class SalesOrderDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesOrderDetail
#         fields = '__all__'

class SalesOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderDetail
        fields = ['id', 'item', 'quantity', 'discount_id', 'price_per_piece', 'discounted_price', 'price_after_discount', 'tax_price', 'price_after_tax', 'sub_total']

class SalesordersSerializer(serializers.ModelSerializer):
    order_details = SalesOrderDetailSerializer(many=True, read_only=True)  # Use read_only=True if you don't want to allow nested writes

    class Meta:
        model = Salesorders
        fields = ['id', 'sales_order_number', 'customer', 'area', 'order_details', 'total_amount', 'discount', 'tax_amount', 'net_total', 'created_at']

    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details', [])  # Extract nested order details
        sales_order = Salesorders.objects.create(**validated_data)  # Create the sales order
        for detail_data in order_details_data:
            SalesOrderDetail.objects.create(sales_order=sales_order, **detail_data)  # Create order details
        return sales_order

class PlaceOrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    area_id = serializers.IntegerField()
    order_details = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            allow_empty=False
        )
    )

    def validate_customer_id(self, value):
        if not Customers.objects.filter(id=value).exists():
            raise serializers.ValidationError("Customer does not exist.")
        return value

    def validate_area_id(self, value):
        if not Area.objects.filter(id=value).exists():
            raise serializers.ValidationError("Area does not exist.")
        return value

    def validate_order_details(self, value):
        for item_detail in value:
            if not Items.objects.filter(id=item_detail.get('item_id')).exists():
                raise serializers.ValidationError(f"Item with ID {item_detail.get('item_id')} does not exist.")
        return value    