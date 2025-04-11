# from rest_framework import viewsets,mixins
# from .models import Categories,SalesOrderDetail, Area, Customers, Discounts, Inventoryadjustments, Items, Purchaseorders, Purchasereceipts, User, SalesorderDiscounts, Salesorders, Salesordertax, Shipments, StockItems, Stockmanagement, Taxconfigurations,  Vendors, Warehouses
# from .serializers import CategoriesSerializer,SalesOrderDetailSerializer,AreaSerializer, CustomersSerializer, DiscountsSerializer, InventoryadjustmentsSerializer, ItemsSerializer, PurchaseordersSerializer, PurchasereceiptsSerializer, SalesorderDiscountsSerializer, SalesordersSerializer, SalesordertaxSerializer, ShipmentsSerializer, StockItemsSerializer, StockmanagementSerializer, TaxconfigurationsSerializer, AuthUserSerializer, VendorsSerializer, WarehousesSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.views import TokenRefreshView
# from .serializers import CustomTokenRefreshSerializer
# from django.db import models

# class CustomTokenRefreshView(TokenRefreshView):
#     serializer_class = CustomTokenRefreshSerializer

# class LoginView(APIView):
#     def post(self, request):
#         # Get username and password from request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Authenticate user
#         user = authenticate(username=username, password=password)

#         if user:
#             # Generate JWT tokens
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'status' : 'success',
#                 'message': 'Login successful',
#                 'data': {
#                       'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh),
#                 },                
              
#             }, status=status.HTTP_200_OK)
#         else:
#             # Invalid credentials
#             return Response({
#                 'message': 'Invalid credentials',
#             }, status=status.HTTP_401_UNAUTHORIZED)

# class CustomCreateMixin(mixins.CreateModelMixin):
#     def create(self, request, *args, **kwargs):
#         # Save the data
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         # Return custom response
#         return Response({
#             "status": "success",
#             "message": "Data created successfully"
#         }, status=status.HTTP_201_CREATED)

# class CustomDestroyMixin(mixins.DestroyModelMixin):
#     def destroy(self, request, *args, **kwargs):
#         # Delete the data
#         instance = self.get_object()
#         self.perform_destroy(instance)

#         # Return custom response
#         return Response({
#             "status": "success",
#             "message": "Data deleted successfully"
#         }, status=status.HTTP_200_OK)


# class CustomUpdateMixin(mixins.UpdateModelMixin):
#     def update(self, request, *args, **kwargs):
#         # Get instance
#         instance = self.get_object()
        
#         # Check for extra fields
#         model_fields = [f.name for f in instance._meta.get_fields()]  # Get all model fields
#         extra_fields = set(request.data.keys()) - set(model_fields)  # Find extra fields
        
#         if extra_fields:
#             return Response({
#                 "status": "error",
#                 "message": f"Invalid fields: {', '.join(extra_fields)}"
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         # Validate and update data
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "status": "success",
#                 "message": "Data updated successfully",
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SalesReportView(APIView):
#     def get(self, request):
#         total_sales = Salesorders.objects.aggregate(total_sales=models.Sum('total_amount'))
#         return Response({'total_sales': total_sales['total_sales']})

# class PurchaseReportView(APIView):
#     def get(self, request):
#         total_purchases = Purchaseorders.objects.aggregate(total_purchases=models.Sum('total_amount'))
#         return Response({'total_purchases': total_purchases['total_purchases']})

# class CategoriesViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Categories.objects.all()
#     serializer_class = CategoriesSerializer
#     permission_classes = [IsAuthenticated]

# class CustomersViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Customers.objects.all()
#     serializer_class = CustomersSerializer
#     permission_classes = [IsAuthenticated]

# class DiscountsViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Discounts.objects.all()
#     serializer_class = DiscountsSerializer
#     permission_classes = [IsAuthenticated]

# class InventoryadjustmentsViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Inventoryadjustments.objects.all()
#     serializer_class = InventoryadjustmentsSerializer
#     permission_classes = [IsAuthenticated]

# class ItemsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Items.objects.all()
#     serializer_class = ItemsSerializer
#     permission_classes = [IsAuthenticated]


# class PurchaseordersViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Purchaseorders.objects.all()
#     serializer_class = PurchaseordersSerializer
#     permission_classes = [IsAuthenticated]

# class PurchasereceiptsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Purchasereceipts.objects.all()
#     serializer_class = PurchasereceiptsSerializer
#     permission_classes = [IsAuthenticated]

# class SalesorderDiscountsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = SalesorderDiscounts.objects.all()
#     serializer_class = SalesorderDiscountsSerializer
#     permission_classes = [IsAuthenticated]

# class SalesordersViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Salesorders.objects.all()
#     serializer_class = SalesordersSerializer
#     permission_classes = [IsAuthenticated]
    
# class SalesordertaxViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Salesordertax.objects.all()
#     serializer_class = SalesordertaxSerializer
#     permission_classes = [IsAuthenticated]
    
# class ShipmentsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Shipments.objects.all()
#     serializer_class = ShipmentsSerializer
#     permission_classes = [IsAuthenticated]
    
# class StockItemsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = StockItems.objects.all()
#     serializer_class = StockItemsSerializer
#     permission_classes = [IsAuthenticated]
    
# class StockmanagementViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Stockmanagement.objects.all()
#     serializer_class = StockmanagementSerializer
#     permission_classes = [IsAuthenticated]
    
# class TaxconfigurationsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Taxconfigurations.objects.all()
#     serializer_class = TaxconfigurationsSerializer
#     permission_classes = [IsAuthenticated]
    
# class AuthUserViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = AuthUserSerializer
#     permission_classes = [IsAuthenticated]
    
# class VendorsViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Vendors.objects.all()
#     serializer_class = VendorsSerializer
#     permission_classes = [IsAuthenticated]
    
# class WarehousesViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Warehouses.objects.all()
#     serializer_class = WarehousesSerializer
#     permission_classes = [IsAuthenticated]
    
    
# class AreaViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Area.objects.all()
#     serializer_class = AreaSerializer
#     permission_classes = [IsAuthenticated]
    
# class SalesOrderDetailViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = SalesOrderDetail.objects.all()
#     serializer_class = SalesOrderDetailSerializer
#     permission_classes = [IsAuthenticated]



# from rest_framework import viewsets,mixins
# from .models import categories, sales_order_return,sales_order_return_detail, purchase_order_return_detail, sales_order_detail, purchase_Order_return, area,purchase_order_detail, customers, discounts, inventory_adjustments, items, purchase_orders, purchase_receipts, user, sales_order_discounts, sales_orders, sales_order_tax,shipments, stock_items, stockmanagement, tax_configurations,  vendors, warehouses
# from .serializers import categories_Serializer, sales_order_return_Serializer, sales_order_return_detail_Serializer, purchase_order_return_detail_Serializer,purchase_order_return_Serializer,purchase_order_detail_Serializer, sales_order_detail_Serializer, place_order_Serializer,area_Serializer, customers_Serializer, discounts_Serializer, inventory_adjustments_Serializer, items_Serializer, purchase_orders_Serializer, purchase_receipts_Serializer, sales_order_discounts_Serializer, sales_orders_Serializer, sales_order_tax_Serializer, shipments_Serializer, stock_items_Serializer, stockmanagement_Serializer, tax_configurations_Serializer, AuthUserSerializer, vendors_Serializer, warehouses_Serializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.views import TokenRefreshView
# from .serializers import CustomTokenRefreshSerializer
# from django.db import models
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.db import transaction
# from django.core.exceptions import ValidationError
# import time
# from django.utils import timezone
# from decimal import Decimal
# from decimal import Decimal
# from django.db import transaction
# from django.utils import timezone


# from django.core.exceptions import ObjectDoesNotExist
# from decimal import Decimal
# from django.utils import timezone
# from django.db import transaction

# def process_return(request_data, user):
#     with transaction.atomic():
#         try:
#             # 1. Validate Input Data
#             required_fields = ['sales_order_id', 'return_details', 'return_reason', 'return_type','user_id']
#             for field in required_fields:
#                 if field not in request_data:
#                     raise ValueError(f"Missing required field: {field}")

#             if request_data['return_type'] not in ['return', 'damage', 'loss']:
#                 raise ValueError("Invalid return type. Must be 'return', 'damage', or 'loss'")

#             # 2. Verify Sales Order exists
#             try:
#                 sales_order = Salesorders.objects.get(id=request_data['sales_order_id'])
#             except Salesorders.DoesNotExist:
#                 raise ValueError(f"Sales Order {request_data['sales_order_id']} does not exist")

#             # 3. Create Return Header
#             details = request_data['return_details'][0]
#             return_header = salesorder_return.objects.create(
#                 sales_order=sales_order,
#                 customer=sales_order.customer,
#                 sales_order_detail_id=details['sales_order_detail_id'],
#                 total_refund_amount=0,
#                 created_at=timezone.now(),
#                 user_id=request_data['user_id']
           
#             )

#             total_refund = Decimal('0')
            
#             # 4. Process Each Return Item
#             for detail in request_data['return_details']:
#                 try:
#                     item_detail = SalesOrderDetail.objects.get(
#                         id=detail['sales_order_detail_id'],
#                         sales_order=sales_order
#                     )
#                 except SalesOrderDetail.DoesNotExist:
#                     raise ValueError(
#                         f"Order detail {detail['sales_order_detail_id']} not found "
#                         f"in order {request_data['sales_order_id']}"
#                     )

#                 # Validate return quantity
#                 if detail['return_quantity'] > item_detail.quantity:
#                     raise ValueError(
#                         f"Return quantity ({detail['return_quantity']}) exceeds "
#                         f"ordered quantity ({item_detail.quantity}) for item {item_detail.item.item_name}"
#                     )

#                 # Convert prices to Decimal for accurate calculations
#                 price_per_piece = Decimal(str(item_detail.price_per_piece))
#                 return_quantity = Decimal(str(detail['return_quantity']))
#                 refund_amount = price_per_piece * return_quantity
#                 total_refund += refund_amount

#                 # Create Return Detail
#                 salesorder_returndetail.objects.create(
#                     returnsale=return_header,
#                     sales_order_detail=item_detail,
#                     item=item_detail.item,
#                     return_quantity=int(detail['return_quantity']),
#                     price_per_piece=item_detail.price_per_piece,
#                     subtotal=int(refund_amount),  # Cast back to int if your model requires
#                     created_at=timezone.now()
#                 )

#                 # Inventory Adjustment
#                 if request_data['return_type'] == 'return':
#                     try:
#                         stock_item = StockItems.objects.get(item=item_detail.item)
#                         stock_item.quantity += int(detail['return_quantity'])
#                         stock_item.save()
#                     except StockItems.DoesNotExist:
#                         raise ValueError(f"No stock record found for item {item_detail.item.item_name}")

#                 # Record inventory adjustment
#                 Inventoryadjustments.objects.create(
#                     item=item_detail.item,
#                     salesorder_return=return_header,
#                     adjustment_type=request_data['return_type'],
#                     quantity=int(detail['return_quantity']),
#                     user=user,
#                     adjustment_reason=request_data['return_reason'],
#                     created_at=timezone.now(),
#                     user_id=request_data['user_id']
#                 )

#             # 5. Update Return Header with Total Refund
#             return_header.total_refund_amount = total_refund
#             return_header.save()

#             # 6. Update Customer Credit (if applicable)
#             if request_data['return_type'] == 'return':
#                 customer = sales_order.customer
#                 customer.total_bill = (customer.total_bill or Decimal('0')) - total_refund
#                 customer.save()

#             return return_header

#         except Exception as e:
#             raise ValueError(f"Return processing failed: {str(e)}")        
        
# class PlaceOrderViewSet(viewsets.ViewSet):
#     @transaction.atomic
#     def create(self, request):
#         serializer = PlaceOrderSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 data = serializer.validated_data
#                 customer_id = data.get('customer_id')
#                 area_id = data.get('area_id')
#                 order_details = data.get('order_details')

#                 # Validate customer
#                 customer = Customers.objects.get(id=customer_id)

#                 # Validate area
#                 area = Area.objects.get(id=area_id)

#                 # Initialize order totals
#                 total_amount = 0
#                 total_discount = 0
#                 total_tax = 0
#                 net_total = 0

#                 # Create sales order
#                 sales_order = Salesorders(
#                     sales_order_number=f"SO{customer_id}{int(time.time())}", 
#                     customer=customer,
#                     area=area,
#                     order_status='Pending',
#                     total_amount=0,  
#                     discount=0,  
#                     tax_amount=0,  
#                     net_total=0, 
#                     created_at=timezone.now()
#                 )
#                 sales_order.save()

#                 # Process each item in the order
#                 for item_detail in order_details:
#                     item_id = item_detail.get('item_id')
#                     quantity = int(item_detail.get('quantity'))  
#                     discount_id = item_detail.get('discount_id')

#                     # Validate item
#                     item = Items.objects.get(id=item_id)

#                     # Retrieve the related StockItems instance
#                     stock_item = item.stock_items.first()  
#                     if not stock_item:
#                         raise ValidationError(f"Item {item.item_name} has no stock information")

#                     # Convert stock_item.quantity to an integer
#                     stock_quantity = int(stock_item.quantity)

#                     # Check stock availability
#                     if stock_quantity < quantity:
#                         raise ValidationError(f"Item {item.item_name} is out of stock")

#                     # Calculate price per piece
#                     price_per_piece = item.item_price

#                     # Apply discount (if applicable)
#                     discounted_price = price_per_piece
#                     if discount_id:
#                         discount = Discounts.objects.get(id=discount_id)
#                         if discount and discount.is_active:
#                             discounted_price = price_per_piece * (1 - discount.discount_percentage / 100)
#                             total_discount += (price_per_piece - discounted_price) * quantity

#                     # Apply tax (if applicable)
#                     tax_price = 0
#                     if item.tax:
#                         tax_price = discounted_price * (item.tax.rate_percentage / 100)
#                         total_tax += tax_price * quantity

#                     # Calculate subtotal for the item
#                     sub_total = (discounted_price + tax_price) * quantity

#                     # Update order totals
#                     total_amount += price_per_piece * quantity
#                     net_total += sub_total

#                     # Create sales order detail
#                     sales_order_detail = SalesOrderDetail(
#                         item=item,
#                         sales_order=sales_order,
#                         price_per_piece=price_per_piece,
#                         quantity=quantity,
#                         discounted_price=discounted_price,
#                         price_after_discount=discounted_price,
#                         tax_price=tax_price,
#                         price_after_tax=discounted_price + tax_price,
#                         sub_total=sub_total
#                     )
#                     sales_order_detail.save()

#                     # Update stock
#                     stock_item.quantity = stock_quantity - quantity
#                     stock_item.save()

#                 # Add delivery charges to the total
#                 net_total += area.delivery_charges

#                 # Update sales order totals
#                 sales_order.total_amount = total_amount
#                 sales_order.discount = total_discount
#                 sales_order.tax_amount = total_tax
#                 sales_order.net_total = net_total
#                 sales_order.save()

#                 # Update customer's total bill
#                 customer.total_bill += net_total
#                 if customer.total_bill > customer.credit_limit:
#                     raise ValidationError("Order exceeds customer's credit limit")
#                 customer.save()

#                 return Response({'message': 'Order placed successfully', 'order_id': sales_order.id}, status=status.HTTP_201_CREATED)

#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# class CustomTokenRefreshView(TokenRefreshView):
#     serializer_class = CustomTokenRefreshSerializer

# class LoginView(APIView):
#     def post(self, request):
        
#         username = request.data.get('username')
#         password = request.data.get('password')

       
#         user = authenticate(username=username, password=password)

#         if user:
            
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'status' : 'success',
#                 'message': 'Login successful',
#                 'data': {
#                       'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh),
#                 },                
              
#             }, status=status.HTTP_200_OK)
#         else:
            
#             return Response({
#                 'message': 'Invalid credentials',
#             }, status=status.HTTP_401_UNAUTHORIZED)

# class CustomCreateMixin(mixins.CreateModelMixin):
#     def create(self, request, *args, **kwargs):       
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

        
#         return Response({
#             "status": "success",
#             "message": "Data created successfully"
#         }, status=status.HTTP_201_CREATED)

# class CustomDestroyMixin(mixins.DestroyModelMixin):
#     def destroy(self, request, *args, **kwargs):
       
#         instance = self.get_object()
#         self.perform_destroy(instance)

       
#         return Response({
#             "status": "success",
#             "message": "Data deleted successfully"
#         }, status=status.HTTP_200_OK)


# class CustomUpdateMixin(mixins.UpdateModelMixin):
#     def update(self, request, *args, **kwargs):
       
#         instance = self.get_object()
        
        
#         model_fields = [f.name for f in instance._meta.get_fields()]  
#         extra_fields = set(request.data.keys()) - set(model_fields)  
        
#         if extra_fields:
#             return Response({
#                 "status": "error",
#                 "message": f"Invalid fields: {', '.join(extra_fields)}"
#             }, status=status.HTTP_400_BAD_REQUEST)
               
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "status": "success",
#                 "message": "Data updated successfully",
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SalesReportView(APIView):
#     def get(self, request):
#         total_sales = Salesorders.objects.aggregate(total_sales=models.Sum('total_amount'))
#         return Response({'total_sales': total_sales['total_sales']})

# class PurchaseReportView(APIView):
#     def get(self, request):
#         total_purchases = Purchaseorders.objects.aggregate(total_purchases=models.Sum('total_amount'))
#         return Response({'total_purchases': total_purchases['total_purchases']})

# class CategoriesViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Categories.objects.all()
#     serializer_class = CategoriesSerializer
#     permission_classes = [IsAuthenticated]

# class CustomersViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Customers.objects.all()
#     serializer_class = CustomersSerializer
#     permission_classes = [IsAuthenticated]

# class DiscountsViewSet(CustomUpdateMixin, CustomCreateMixin, CustomDestroyMixin, viewsets.ModelViewSet):
#     queryset = Discounts.objects.all()
#     serializer_class = DiscountsSerializer
#     permission_classes = [IsAuthenticated]
    
# class InventoryadjustmentsViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Inventoryadjustments.objects.all()
#     serializer_class = InventoryadjustmentsSerializer
#     permission_classes = [IsAuthenticated]

# class ItemsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Items.objects.all()
#     serializer_class = ItemsSerializer
#     permission_classes = [IsAuthenticated]

# class salesorder_returnViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = salesorder_return.objects.all()
#     serializer_class = salesorder_returnSerializer
#     permission_classes = [IsAuthenticated]
    
#     def create(self, request, *args, **kwargs):
#         try:
#             return_data = request.data
#             return_instance = process_return(return_data, request.user)
#             serializer = self.get_serializer(return_instance)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValueError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
# class PurchaseOrder_returnViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = PurchaseOrder_return.objects.all()
#     serializer_class = PurchaseOrder_returnSerializer
#     permission_classes = [IsAuthenticated]

# class PurchaseOrder_returndetailViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = PurchaseOrder_returndetail.objects.all()
#     serializer_class = PurchaseOrder_returndetailSerializer
#     permission_classes = [IsAuthenticated]

# class PurchaseordersViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Purchaseorders.objects.all()
#     serializer_class = PurchaseordersSerializer
#     permission_classes = [IsAuthenticated]

# class PurchaseOrderDetailViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = PurchaseOrderDetail.objects.all()
#     serializer_class = PurchaseOrderDetailSerializer
#     permission_classes = [IsAuthenticated]


# # class PurchaseOrderDetailSummaryViewSet(APIView):
# #     def get(self, request):
# #         total_sales = Salesorders.objects.aggregate(total_sales=models.Sum('total_amount'))
# #         return Response({'total_sales': total_sales['total_sales']})


# class PurchasereceiptsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Purchasereceipts.objects.all()
#     serializer_class = PurchasereceiptsSerializer
#     permission_classes = [IsAuthenticated]

# class SalesorderDiscountsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = SalesorderDiscounts.objects.all()
#     serializer_class = SalesorderDiscountsSerializer
#     permission_classes = [IsAuthenticated]

# class SalesordersViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Salesorders.objects.all()
#     serializer_class = SalesordersSerializer
#     permission_classes = [IsAuthenticated]
    
# class salesorder_returndetailViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = salesorder_returndetail.objects.all()
#     serializer_class = salesorder_returndetailSerializer
#     permission_classes = [IsAuthenticated]

# class SalesordertaxViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Salesordertax.objects.all()
#     serializer_class = SalesordertaxSerializer
#     permission_classes = [IsAuthenticated]

    
# class ShipmentsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Shipments.objects.all()
#     serializer_class = ShipmentsSerializer
#     permission_classes = [IsAuthenticated]
    
# class StockItemsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = StockItems.objects.all()
#     serializer_class = StockItemsSerializer
#     permission_classes = [IsAuthenticated]
    
# class StockmanagementViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Stockmanagement.objects.all()
#     serializer_class = StockmanagementSerializer
#     permission_classes = [IsAuthenticated]
    
# class TaxconfigurationsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Taxconfigurations.objects.all()
#     serializer_class = TaxconfigurationsSerializer
#     permission_classes = [IsAuthenticated]
    
# class AuthUserViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = AuthUserSerializer
#     permission_classes = [IsAuthenticated]
    
# class VendorsViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Vendors.objects.all()
#     serializer_class = VendorsSerializer
#     permission_classes = [IsAuthenticated]
    
# class WarehousesViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = Warehouses.objects.all()
#     serializer_class = WarehousesSerializer
#     permission_classes = [IsAuthenticated]
    
    
# class AreaViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = Area.objects.all()
#     serializer_class = AreaSerializer
#     permission_classes = [IsAuthenticated]
    
# class SalesOrderDetailViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = SalesOrderDetail.objects.all()
#     serializer_class = SalesOrderDetailSerializer
#     permission_classes = [IsAuthenticated]
    
    
    

from rest_framework import viewsets,mixins
from .models import categories, sales_order_return,sales_order_return_detail, purchase_order_return_detail, sales_order_detail, purchase_order_return, area,purchase_order_detail, customers, discounts, inventory_adjustments, items, purchase_orders, purchase_receipts, User, sales_order_discounts, sales_orders, sales_order_tax,shipments, stock_items, stockmanagement, tax_configurations,  vendors, warehouses
from .serializers import categories_Serializer, sales_order_return_Serializer, sales_order_return_detail_Serializer, purchase_order_return_detail_Serializer,purchase_order_return_Serializer,purchase_order_detail_Serializer, sales_order_detail_Serializer, place_order_Serializer,area_Serializer, customers_Serializer, discounts_Serializer, inventory_adjustments_Serializer, items_Serializer, purchase_orders_Serializer, purchase_receipts_Serializer, sales_order_discounts_Serializer, sale_orders_Serializer, sales_order_tax_Serializer, shipments_Serializer, stock_items_Serializer, stockmanagement_Serializer, tax_configurations_Serializer, AuthUserSerializer, vendors_Serializer, warehouses_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomTokenRefreshSerializer
from django.db import models
from rest_framework import viewsets, status
from django.core.exceptions import ValidationError
import time
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def process_return(request_data, user):
    with transaction.atomic():
        try:
            # 1. Validate Input Data
            required_fields = ['sales_order_id', 'return_details', 'return_reason', 'return_type', 'created_by']
            for field in required_fields:
                if field not in request_data:
                    raise ValueError(f"Missing required field: {field}")

            if request_data['return_type'] not in ['return', 'damage', 'loss']:
                raise ValueError("Invalid return type. Must be 'return', 'damage', or 'loss'")

            try:
                create_by_user = User.objects.get(id=request_data['created_by'])
            except User.DoesNotExist:
                raise ValueError(f"User with ID {request_data['created_by']} does not exist")
                    
            # 2. Verify Sales Order exists
            try:
                sales_order = sales_orders.objects.get(id=request_data['sales_order_id'])
            except sales_orders.DoesNotExist:
                raise ValueError(f"Sales Order {request_data['sales_order_id']} does not exist")
            
            # Verify Sales order detail 
            sales_detail_id = request_data['return_details'][0]['sales_order_detail_id']
            try:
                sales_detail_id = sales_order_detail.objects.get(
                    id=sales_detail_id,
                    sales_order=sales_order
                )
            except sales_order_detail.DoesNotExist:
                raise ValueError(f"Order detail {sales_detail_id} not found in order {request_data['sales_order_id']}")

            # 3. Create Return Header
            return_header = sales_order_return.objects.create(
                sales_order=sales_order,
                customer=sales_order.customer,
                total_refund_amount=0,
                sales_order_detail=sales_detail_id,
                created_at=timezone.now(),
                created_by=create_by_user
            )

            total_refund = Decimal('0')
            
            # 4. Process Each Return Item
            for detail in request_data['return_details']:
                try:
                    item_detail = sales_order_detail.objects.get(
                        id=detail['sales_order_detail_id'],
                        sales_order=sales_order
                    )
                except sales_order_detail.DoesNotExist:
                    raise ValueError(
                        f"Order detail {detail['sales_order_detail_id']} not found "
                        f"in order {request_data['sales_order_id']}"
                    )

                # Validate return quantity
                if detail['return_quantity'] > item_detail.quantity:
                    raise ValueError(
                        f"Return quantity ({detail['return_quantity']}) exceeds "
                        f"ordered quantity ({item_detail.quantity}) for item {item_detail.item.item_name}"
                    )

                # Convert prices to Decimal for accurate calculations
                price_per_piece = Decimal(str(item_detail.price_per_piece))
                return_quantity = Decimal(str(detail['return_quantity']))
                refund_amount = price_per_piece * return_quantity
                total_refund += refund_amount

                # Create Return Detail
                sales_order_return_detail.objects.create(
                    return_sale=return_header,
                    sales_order_detail=item_detail,
                    item=item_detail.item,
                    return_quantity=int(detail['return_quantity']),
                    price_per_piece=item_detail.price_per_piece,
                    subtotal=refund_amount,  
                    created_at=timezone.now()
                )

                # Inventory Adjustment
                if request_data['return_type'] == 'return':
                    try:
                        stock_item = stock_items.objects.get(item=item_detail.item)
                        stock_item.quantity += int(detail['return_quantity'])
                        stock_item.save()
                    except stock_items.DoesNotExist:
                        raise ValueError(f"No stock record found for item {item_detail.item.item_name}")


                inventory_adjustments.objects.create(
                    item=item_detail.item,
                    sales_order_return=return_header,
                    adjustment_type=request_data['return_type'],
                    quantity=int(detail['return_quantity']),
                    adjustment_reason=request_data['return_reason'],
                    created_at=timezone.now(),
                    adjusted_by=create_by_user 
                )

            # 5. Update Return Header with Total Refund
            return_header.total_refund_amount = total_refund
            return_header.save()

            # 6. Update Customer Credit (if applicable)
            if request_data['return_type'] == 'return':
                customer = sales_order.customer
                customer.total_bill = (customer.total_bill or Decimal('0')) - total_refund
                customer.save()

            return return_header

        except Exception as e:
            raise ValueError(f"Return processing failed: {str(e)}")
        
                
class PlaceOrderViewSet(viewsets.ViewSet):
    @transaction.atomic
    def create(self, request):
        serializer = place_order_Serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                customer_id = data.get('customer_id')
                area_id = data.get('area_id')
                order_details = data.get('order_details')

                # Validate customer
                customer = customers.objects.get(id=customer_id)

                # Validate area
                area_obj = area.objects.get(id=area_id)

                # Initialize order totals
                total_amount = 0
                total_discount = 0
                total_tax = 0
                net_total = 0

                # Create sales order
                sales_order = sales_orders(
                    sales_order_number=f"SO{customer_id}{int(time.time())}", 
                    customer=customer,
                    area=area_obj,
                    order_status='Pending',
                    total_amount=0,  
                    discount=0,  
                    tax_amount=0,  
                    net_total=0, 
                    created_at=timezone.now()
                )
                sales_order.save()

                # Process each item in the order
                for item_detail in order_details:
                    item_id = item_detail.get('item_id')
                    quantity = int(item_detail.get('quantity'))  
                    discount_id = item_detail.get('discount_id')

                    # Validate item
                    item = items.objects.get(id=item_id)

                    # Retrieve the related StockItems instance
                    stock_item = item.stock_items.first()  
                    if not stock_item:
                        raise ValidationError(f"Item {item.item_name} has no stock information")

                    # Convert stock_item.quantity to an integer
                    stock_quantity = int(stock_item.quantity)

                    # Check stock availability
                    if stock_quantity < quantity:
                        raise ValidationError(f"Item {item.item_name} is out of stock")

                    # Calculate price per piece
                    price_per_piece = item.item_price

                    # Apply discount (if applicable)
                    discounted_price = price_per_piece
                    if discount_id:
                        discount = discounts.objects.get(id=discount_id)
                        if discount and discount.is_active:
                            discounted_price = price_per_piece * (1 - discount.discount_percentage / 100)
                            total_discount += (price_per_piece - discounted_price) * quantity

                    # Apply tax (if applicable)
                    tax_price = 0
                    if item.tax:
                        tax_price = discounted_price * (item.tax.rate_percentage / 100)
                        total_tax += tax_price * quantity

                    # Calculate subtotal for the item
                    sub_total = (discounted_price + tax_price) * quantity

                    # Update order totals
                    total_amount += price_per_piece * quantity
                    net_total += sub_total

                    # Create sales order detail
                    sales_order_detail_obj = sales_order_detail(
                        item=item,
                        sales_order=sales_order,
                        price_per_piece=price_per_piece,
                        quantity=quantity,
                        discounted_price=discounted_price,
                        price_after_discount=discounted_price,
                        tax_price=tax_price,
                        price_after_tax=discounted_price + tax_price,
                        sub_total=sub_total
                    )
                    sales_order_detail_obj.save()

                    # Update stock
                    stock_item.quantity = stock_quantity - quantity
                    stock_item.save()

                # Add delivery charges to the total
                net_total += area_obj.delivery_charges

                # Update sales order totals
                sales_order.total_amount = total_amount
                sales_order.discount = total_discount
                sales_order.tax_amount = total_tax
                sales_order.net_total = net_total
                sales_order.save()

                # Update customer's total bill
                customer.total_bill += net_total
                if customer.total_bill > customer.credit_limit:
                    raise ValidationError("Order exceeds customer's credit limit")
                customer.save()

                return Response({'message': 'Order placed successfully', 'order_id': sales_order.id}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class LoginView(APIView):
    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')

       
        user = authenticate(username=username, password=password)

        if user:
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'status' : 'success',
                'message': 'Login successful',
                'data': {
                      'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                },                
              
            }, status=status.HTTP_200_OK)
        else:
            
            return Response({
                'message': 'Invalid credentials',
            }, status=status.HTTP_401_UNAUTHORIZED)

class CustomCreateMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        
        return Response({
            "status": "success",
            "message": "Data created successfully"
        }, status=status.HTTP_201_CREATED)

class CustomDestroyMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
       
        instance = self.get_object()
        self.perform_destroy(instance)

       
        return Response({
            "status": "success",
            "message": "Data deleted successfully"
        }, status=status.HTTP_200_OK)


class CustomUpdateMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
       
        instance = self.get_object()
        
        
        model_fields = [f.name for f in instance._meta.get_fields()]  
        extra_fields = set(request.data.keys()) - set(model_fields)  
        
        if extra_fields:
            return Response({
                "status": "error",
                "message": f"Invalid fields: {', '.join(extra_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)
               
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Data updated successfully",
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesReportView(APIView):
    def get(self, request):
        total_sales = sales_orders.objects.aggregate(total_sales=models.Sum('total_amount'))
        return Response({'total_sales': total_sales['total_sales']})

class PurchaseReportView(APIView):
    def get(self, request):
        total_purchases = purchase_orders.objects.aggregate(total_purchases=models.Sum('total_amount'))
        return Response({'total_purchases': total_purchases['total_purchases']})

class categories_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = categories.objects.all()
    serializer_class = categories_Serializer
    permission_classes = [IsAuthenticated]

class customers_ViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = customers.objects.all()
    serializer_class = customers_Serializer
    permission_classes = [IsAuthenticated]

class discounts_ViewSet(CustomUpdateMixin, CustomCreateMixin, CustomDestroyMixin, viewsets.ModelViewSet):
    queryset = discounts.objects.all()
    serializer_class = discounts_Serializer
    permission_classes = [IsAuthenticated]
    
class inventory_adjustments_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = inventory_adjustments.objects.all()
    serializer_class = inventory_adjustments_Serializer
    permission_classes = [IsAuthenticated]

class items_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = items.objects.all()
    serializer_class = items_Serializer
    permission_classes = [IsAuthenticated]

class sales_order_return_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = sales_order_return.objects.all()
    serializer_class = sales_order_return_Serializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        try:
            return_data = request.data
            return_instance = process_return(return_data, request.user)
            serializer = self.get_serializer(return_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
class purchase_order_return_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = purchase_order_return.objects.all()
    serializer_class = purchase_order_return_Serializer
    permission_classes = [IsAuthenticated]

class purchase_order_return_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = purchase_order_return_detail.objects.all()
    serializer_class = purchase_order_return_detail_Serializer
    permission_classes = [IsAuthenticated]

class purchase_orders_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = purchase_orders.objects.all()
    serializer_class = purchase_orders_Serializer
    permission_classes = [IsAuthenticated]

class purchase_order_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = purchase_order_detail.objects.all()
    serializer_class = purchase_order_detail_Serializer
    permission_classes = [IsAuthenticated]


# class PurchaseOrderDetailSummaryViewSet(APIView):
#     def get(self, request):
#         total_sales = Salesorders.objects.aggregate(total_sales=models.Sum('total_amount'))
#         return Response({'total_sales': total_sales['total_sales']})


class purchase_receipts_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = purchase_receipts.objects.all()
    serializer_class = purchase_receipts_Serializer
    permission_classes = [IsAuthenticated]

class sales_order_discounts_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = sales_order_discounts.objects.all()
    serializer_class = sales_order_discounts_Serializer
    permission_classes = [IsAuthenticated]

class sales_orders_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = sales_orders.objects.all()
    serializer_class = sale_orders_Serializer
    permission_classes = [IsAuthenticated]
    
class sales_order_return_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = sales_order_return_detail.objects.all()
    serializer_class = sales_order_return_detail_Serializer
    permission_classes = [IsAuthenticated]

class sales_order_tax_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = sales_order_tax.objects.all()
    serializer_class = sales_order_tax_Serializer
    permission_classes = [IsAuthenticated]

    
class shipments_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = shipments.objects.all()
    serializer_class = shipments_Serializer
    permission_classes = [IsAuthenticated]
    
class stock_items_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = stock_items.objects.all()
    serializer_class = stock_items_Serializer
    permission_classes = [IsAuthenticated]
    
class stockmanagement_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = stockmanagement.objects.all()
    serializer_class = stockmanagement_Serializer
    permission_classes = [IsAuthenticated]
    
class tax_configurations_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = tax_configurations.objects.all()
    serializer_class = tax_configurations_Serializer
    permission_classes = [IsAuthenticated]
    
class AuthUser_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = [IsAuthenticated]
    
class vendors_ViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = vendors.objects.all()
    serializer_class = vendors_Serializer
    permission_classes = [IsAuthenticated]
    
class warehouses_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = warehouses.objects.all()
    serializer_class = warehouses_Serializer
    permission_classes = [IsAuthenticated]
    
    
class area_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = area.objects.all()
    serializer_class = area_Serializer
    permission_classes = [IsAuthenticated]
    
class sales_order_detail_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = sales_order_detail.objects.all()
    serializer_class = sales_order_detail_Serializer
    permission_classes = [IsAuthenticated]
        
    