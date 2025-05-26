from rest_framework import serializers
from .models import receive_note, warehouse_stock, transfer_note,store, request_note, categories, sales_order_return,sales_order_return_detail,notification, purchase_order_return_detail, sales_order_detail, purchase_order_return, area,purchase_order_detail, customers, discounts, inventory_adjustments, items, purchase_orders, purchase_receipts, User, sales_order_discounts, sales_orders, sales_order_tax,shipments, stock_items, stockmanagement, tax_configurations,  vendors, warehouses

from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  

        
        return {
            "status": "success",
            "message": "Token refreshed successfully",
            "data": {
                "access_token": data["access"]
            }
        }

class purchase_order_return_Serializer(serializers.ModelSerializer):
    adjustment_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    class Meta:
        model = purchase_order_return
        fields = ['adjustment_ids']

    def validate_adjustment_ids(self, value):
        if not value:
            raise serializers.ValidationError("At least one adjustment ID is required")
        
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate adjustment IDs are not allowed")
            
        return value
        
class purchase_order_detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = purchase_order_detail
        fields = '__all__'
        
        
class purchase_order_return_detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = purchase_order_return_detail
        fields = '__all__'

class sales_order_return_Serializer(serializers.ModelSerializer):
    class Meta:
        model = sales_order_return
        fields = '__all__'

class categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = '__all__'

class customers_Serializer(serializers.ModelSerializer):
    class Meta:
        model = customers
        fields = '__all__'

class discounts_Serializer(serializers.ModelSerializer):
    class Meta:
        model = discounts
        fields = '__all__'
        
        
class inventory_adjustments_Serializer(serializers.ModelSerializer):
    class Meta:
        model = inventory_adjustments
        fields = [
            'item',
            'quantity',
            'adjustment_type',
            'adjustment_reason',
            'adjusted_by'
        ]
        extra_kwargs = {
            'item': {'required': True},
            'quantity': {'required': True, 'min_value': 1},
            'adjustment_type': {'required': True},
            'adjusted_by': {'required': True}
        }

    def validate_adjusted_by(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
    
            
class items_Serializer(serializers.ModelSerializer):
    class Meta:
        model = items
        fields = '__all__'


class notification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = notification
        fields = '__all__'

class purchase_orders_Serializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(required=True)
    order_details = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )

    class Meta:
        model = purchase_orders
        exclude = ['total_amount', 'discount', 'tax_amount', 'net_total', 'purchase_order_number']    
        
class purchase_receipts_Serializer(serializers.ModelSerializer):
    class Meta:
        model = purchase_receipts
        fields = '__all__'

class sales_order_discounts_Serializer(serializers.ModelSerializer):
    class Meta:
        model = sales_order_discounts
        fields = '__all__'

# class SalesordersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Salesorders
#         fields = '__all__'

class sales_order_tax_Serializer(serializers.ModelSerializer):
    class Meta:
        model = sales_order_tax
        fields = '__all__'

class shipments_Serializer(serializers.ModelSerializer):
    class Meta:
        model = shipments
        fields = '__all__'

class stock_items_Serializer(serializers.ModelSerializer):
    class Meta:
        model = stock_items
        fields = '__all__'

class sales_order_return_detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = sales_order_return_detail
        fields = '__all__'

class stockmanagement_Serializer(serializers.ModelSerializer):
    class Meta:
        model = stockmanagement
        fields = '__all__'

class store_Serializer(serializers.ModelSerializer):
    class Meta:
        model = store
        fields = '__all__'
        
class request_note_Serializer(serializers.ModelSerializer):
    class Meta:
        model = request_note
        fields = '__all__'
        
class transfer_note_Serializer(serializers.ModelSerializer):
    class Meta:
        model = transfer_note
        fields = '__all__'
class warehouse_stock_Serializer(serializers.ModelSerializer):
    class Meta:
        model = warehouse_stock
        fields = '__all__'

class receive_note_Serializer(serializers.ModelSerializer):
    class Meta:
        model = receive_note
        fields = '__all__'                        

class tax_configurations_Serializer(serializers.ModelSerializer):
    class Meta:
        model = tax_configurations
        fields = '__all__'

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class vendors_Serializer(serializers.ModelSerializer):
    class Meta:
        model = vendors
        fields = '__all__'

class warehouses_Serializer(serializers.ModelSerializer):
    class Meta:
        model = warehouses
        fields = '__all__'
        
        
class area_Serializer(serializers.ModelSerializer):
    class Meta:
        model = area
        fields = '__all__'
        
# class SalesOrderDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesOrderDetail
#         fields = '__all__'

class sales_order_detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = sales_order_detail
        fields = ['id', 'item', 'quantity', 'discount_id', 'price_per_piece', 'discounted_price', 'price_after_discount', 'tax_price', 'price_after_tax', 'sub_total']

class sale_orders_Serializer(serializers.ModelSerializer):
    order_details = sales_order_detail_Serializer(many=True, read_only=True)  # Use read_only=True if you don't want to allow nested writes

    class Meta:
        model = sales_orders
        fields = ['id', 'sales_order_number', 'customer', 'area', 'order_details', 'total_amount', 'discount', 'tax_amount', 'net_total', 'created_at']

    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details', [])  # Extract nested order details
        sales_order = sales_orders.objects.create(**validated_data)  # Create the sales order
        for detail_data in order_details_data:
            sales_order_detail.objects.create(sales_order=sales_order, **detail_data)  # Create order details
        return sales_order

class place_order_Serializer(serializers.Serializer):
    customer_id = serializers.IntegerField(required=True)
    area_id = serializers.IntegerField(required=False, allow_null=True)  # Make this optional
    order_details = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            allow_empty=False
        ),
        required=True
    )    
class SalesReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_orders = serializers.IntegerField()
    total_items_sold = serializers.IntegerField()
    
    
    