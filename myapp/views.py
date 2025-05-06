from rest_framework import viewsets,mixins
from .models import categories, sales_order_return,sales_order_return_detail,notification, purchase_order_return_detail, sales_order_detail, purchase_order_return, area,purchase_order_detail, customers, discounts, inventory_adjustments, items, purchase_orders, purchase_receipts, User, sales_order_discounts, sales_orders, sales_order_tax,shipments, stock_items, stockmanagement, tax_configurations,  vendors, warehouses
from .serializers import categories_Serializer, sales_order_return_Serializer,notification_Serializer, sales_order_return_detail_Serializer, purchase_order_return_detail_Serializer,purchase_order_return_Serializer,purchase_order_detail_Serializer, sales_order_detail_Serializer, place_order_Serializer,area_Serializer, customers_Serializer, discounts_Serializer, inventory_adjustments_Serializer, items_Serializer, purchase_orders_Serializer, purchase_receipts_Serializer, sales_order_discounts_Serializer, sale_orders_Serializer, sales_order_tax_Serializer, shipments_Serializer, stock_items_Serializer, stockmanagement_Serializer, tax_configurations_Serializer, AuthUserSerializer, vendors_Serializer, warehouses_Serializer
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomTokenRefreshSerializer
from django.db import models
from rest_framework import status
from django.core.exceptions import ValidationError
import time
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import async_to_sync
from django.shortcuts import render
from channels.layers import get_channel_layer
from django.db.models import Sum, Count,F
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View

# class purchaseordersViewSet(viewsets.ModelViewSet):
#     queryset = purchase_orders.objects.all()
#     serializer_class = purchase_orders_Serializer
#     permission_classes = [IsAuthenticated]
    
#     @transaction.atomic
#     def create(self, request):
#         serializer = purchase_orders_Serializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 data = serializer.validated_data
#                 vendor_id = data.get('vendor_id')
#                 order_details = data.get('order_details')

#                 # Validate vendor
#                 vendor = vendors.objects.get(id=vendor_id)

#                 # Initialize order totals
#                 total_amount = Decimal('0')
#                 total_discount = Decimal('0')
#                 total_tax = Decimal('0')
#                 net_total = Decimal('0')

#                 # Create purchase order with initial values
#                 purchase_order = purchase_orders(
#                     purchase_order_number=f"PO{vendor_id}{int(time.time())}",
#                     vendor=vendor,
#                     order_status='Pending',
#                     total_amount=0,  
#                     discount=0,      
#                     tax_amount=0,    
#                     net_total=0,     
#                     created_at=timezone.now()
#                 )
#                 purchase_order.save()

#                 # Process each item in the order
#                 for item_detail in order_details:
#                     item_id = item_detail.get('item_id')
#                     item_name = item_detail.get('item_name', f"Item-{item_id}")
#                     quantity = int(item_detail.get('quantity'))
#                     price_per_piece = Decimal(str(item_detail.get('price_per_piece')))
#                     discount_percentage = Decimal(str(item_detail.get('discount_percentage', 0)))
#                     tax_percentage = Decimal(str(item_detail.get('tax_percentage', 0)))
#                     category_name = item_detail.get('category_name', 'Uncategorized')

#                     # Get or create item
#                     item, item_created = items.objects.get_or_create(
#                         id=item_id,
#                         defaults={
#                             'item_name': item_name,
#                             'item_code': f"ITEM-{item_id}",
#                             'sku': f"SKU-{item_id}",
#                             'item_price': price_per_piece,
#                             'item_type': 'Good',
#                             'created_at': timezone.now()
#                         }
#                     )

#                     # Get or create category
#                     category, _ = categories.objects.get_or_create(
#                         category_name=category_name,
#                         defaults={
#                             'category_desc': f"Auto-created for {item_name}",
#                             'created_at': timezone.now()
#                         }
#                     )

#                     # Assign category if new item
#                     if item_created:
#                         item.category = category
#                         item.save()

#                     # Calculate financials
#                     item_total = price_per_piece * quantity
#                     discount_amount = item_total * (discount_percentage / Decimal('100'))
#                     discounted_price = item_total - discount_amount
#                     tax_amount = discounted_price * (tax_percentage / Decimal('100'))
#                     sub_total = discounted_price + tax_amount

#                     # Update order totals
#                     total_amount += item_total
#                     total_discount += discount_amount
#                     total_tax += tax_amount
#                     net_total += sub_total

#                     # Create purchase order detail
#                     purchase_order_detail.objects.create(
#                         item=item,
#                         # category=category,
#                         purchase_order=purchase_order,
#                         quantity=quantity,
#                         price_per_piece=price_per_piece,
#                         discounted_price=discounted_price/quantity, 
#                         price_after_discount=discounted_price,
#                         tax_price=tax_amount,
#                         price_after_tax=sub_total,
#                         sub_total=sub_total
#                     )

#                     # Update or create stock
#                     if item.item_type == 'Good':
#                         stock_item, created = stock_items.objects.get_or_create(
#                             item=item,
#                             defaults={
#                                 'quantity': quantity,
#                                 'safety_stock_level': 10,
#                                 'last_restocked_at': timezone.now()
#                             }
#                         )
#                         if not created:
#                             stock_item.quantity += quantity
#                             stock_item.last_restocked_at = timezone.now()
#                             stock_item.save()

#                 # Update purchase order with final totals
#                 purchase_order.total_amount = total_amount
#                 purchase_order.discount = total_discount
#                 purchase_order.tax_amount = total_tax
#                 purchase_order.net_total = net_total
#                 purchase_order.save()

#                 return Response({
#                     'message': 'Purchase order created successfully',
#                     'order_id': purchase_order.id,
#                     'purchase_order_number': purchase_order.purchase_order_number,
#                     'total_amount': str(total_amount),
#                     'net_total': str(net_total)
#                 }, status=status.HTTP_201_CREATED)

#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def process_return(request_data, user):
#     with transaction.atomic():
#         try:
#             # 1. Validate Input Data
#             required_fields = ['sales_order_id', 'return_details', 'return_reason', 'return_type', 'created_by']
#             for field in required_fields:
#                 if field not in request_data:
#                     raise ValueError(f"Missing required field: {field}")

#             valid_return_types = ['return', 'damage', 'loss']
#             if request_data['return_type'] not in valid_return_types:
#                 raise ValueError(f"Invalid return type. Must be one of: {', '.join(valid_return_types)}")

#             try:
#                 create_by_user = User.objects.get(id=request_data['created_by'])
#             except User.DoesNotExist:
#                 raise ValueError(f"User with ID {request_data['created_by']} does not exist")
                    
#             # 2. Verify Sales Order exists
#             try:
#                 sales_order = sales_orders.objects.get(id=request_data['sales_order_id'])
#             except sales_orders.DoesNotExist:
#                 raise ValueError(f"Sales Order {request_data['sales_order_id']} does not exist")
            
#             # Verify Sales order detail 
#             sales_detail_id = request_data['return_details'][0]['sales_order_detail_id']
#             try:
#                 sales_detail = sales_order_detail.objects.get(
#                     id=sales_detail_id,
#                     sales_order=sales_order
#                 )
#             except sales_order_detail.DoesNotExist:
#                 raise ValueError(f"Order detail {sales_detail_id} not found in order {request_data['sales_order_id']}")

#             # 3. Create Return Header with return_type
#             return_header = sales_order_return.objects.create(
#                 sales_order=sales_order,
#                 customer=sales_order.customer,
#                 total_refund_amount=0,
#                 sales_order_detail=sales_detail,
#                 return_type=request_data['return_type'],  
#                 return_reason=request_data['return_reason'],  
#                 created_at=timezone.now(),
#                 created_by=create_by_user
#             )

#             total_refund = Decimal('0')
            
#             # 4. Process Each Return Item
#             for detail in request_data['return_details']:
#                 try:
#                     item_detail = sales_order_detail.objects.get(
#                         id=detail['sales_order_detail_id'],
#                         sales_order=sales_order
#                     )
#                 except sales_order_detail.DoesNotExist:
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
#                 sales_order_return_detail.objects.create(
#                     return_sale=return_header,
#                     sales_order_detail=item_detail,
#                     item=item_detail.item,
#                     return_quantity=int(detail['return_quantity']),
#                     price_per_piece=item_detail.price_per_piece,
#                     subtotal=refund_amount,  
#                     created_at=timezone.now()
#                 )

#                 # Inventory Adjustment
#                 if request_data['return_type'] == 'return':
#                     try:
#                         stock_item = stock_items.objects.get(item=item_detail.item)
#                         stock_item.quantity += int(detail['return_quantity'])
#                         stock_item.save()
#                     except stock_items.DoesNotExist:
#                         raise ValueError(f"No stock record found for item {item_detail.item.item_name}")

#                 # Create inventory adjustment with the same return_type
#                 inventory_adjustments.objects.create(
#                     item=item_detail.item,
#                     sales_order_return=return_header,
#                     adjustment_type=request_data['return_type'],
#                     quantity=int(detail['return_quantity']),
#                     adjustment_reason=request_data['return_reason'],
#                     created_at=timezone.now(),
#                     adjusted_by=create_by_user 
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



# class notification_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = notification.objects.all()
#     serializer_class = notification_Serializer
#     permission_classes = [IsAuthenticated]

# # def check_safety_stock(item):
# #         stock = stock_items.objects.get(item=item)
# #         if stock.quantity <= stock.safety_stock_level:
# #             # Check if notification already exists
# #             if not notification.objects.filter(item=item, is_read=False).exists():
# #                 notification.objects.create(
# #                     item=item,
# #                     message=f"Stock for '{item.item_name}' has fallen below the safety level.",
# #                     created_at=timezone.now(),
# #                     is_read=False
# #                 )
# #                 # Optional: Send to WebSocket
# #                 from asgiref.sync import async_to_sync
# #                 from channels.layers import get_channel_layer
                
# #                 channel_layer = get_channel_layer()
# #                 async_to_sync(channel_layer.group_send)(
# #                     "notifications",  
# #                     {
# #                         "type": "send_notification",
# #                         "message": f"Restock '{item.item_name}'! Low stock alert."
# #                     }
# #                 )
    
    
# class PlaceOrderViewSet(viewsets.ViewSet):
#     @transaction.atomic
#     def create(self, request):
#         serializer = place_order_Serializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 data = serializer.validated_data
#                 customer_id = data.get('customer_id')
#                 area_id = data.get('area_id')
#                 order_details = data.get('order_details')

#                 # Validate customer
#                 customer = customers.objects.get(id=customer_id)

#                 # Validate area
#                 area_obj = area.objects.get(id=area_id)

#                 # Initialize order totals
#                 total_amount = 0
#                 total_discount = 0
#                 total_tax = 0
#                 net_total = 0

#                 # Create sales order
#                 sales_order = sales_orders(
#                     sales_order_number=f"SO{customer_id}{int(time.time())}", 
#                     customer=customer,
#                     area=area_obj,
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
#                     item = items.objects.get(id=item_id)

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

#                     # Apply discount
#                     discounted_price = price_per_piece
#                     if discount_id:
#                         discount = discounts.objects.get(id=discount_id)
#                         if discount and discount.is_active:
#                             discounted_price = price_per_piece * (1 - discount.discount_percentage / 100)
#                             total_discount += (price_per_piece - discounted_price) * quantity

                   
#                     tax_price = 0
#                     if item.tax:
#                         tax_price = discounted_price * (item.tax.rate_percentage / 100)
#                         total_tax += tax_price * quantity

                    
#                     sub_total = (discounted_price + tax_price) * quantity

                    
#                     total_amount += price_per_piece * quantity
#                     net_total += sub_total

                    
#                     sales_order_detail_obj = sales_order_detail(
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
#                     sales_order_detail_obj.save()

                    
#                     stock_item.quantity = stock_quantity - quantity
#                     stock_item.save()
#                     check_safety_stock(item)

                
#                 net_total += area_obj.delivery_charges

                
#                 sales_order.total_amount = total_amount
#                 sales_order.discount = total_discount
#                 sales_order.tax_amount = total_tax
#                 sales_order.net_total = net_total
#                 sales_order.save()

                
#                 customer.total_bill += net_total
#                 if customer.total_bill > customer.credit_limit:
#                     raise ValidationError("Order exceeds customer's credit limit")
#                 customer.save()

#                 return Response({'message': 'Order placed successfully', 'order_id': sales_order.id}, status=status.HTTP_201_CREATED)

#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
# class SalesReportView(APIView):
#     def get(self, request):
#         total_sales = sales_orders.objects.aggregate(total_sales=models.Sum('total_amount')) 
#         return Response({'total_sales': total_sales['total_sales']})

# class PurchaseReportView(APIView):
#     def get(self, request):
#         total_purchases = purchase_orders.objects.aggregate(total_purchases=models.Sum('total_amount'))
#         return Response({'total_purchases': total_purchases['total_purchases']})

# class categories_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = categories.objects.all()
#     serializer_class = categories_Serializer
#     permission_classes = [IsAuthenticated]
    
# def categories_list_view(request):
#     all_categories = categories.objects.all()
#     return render(request, 'categories_list.html', {'categories': all_categories})
    

# class customers_ViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = customers.objects.all()
#     serializer_class = customers_Serializer
#     permission_classes = [IsAuthenticated]

# class discounts_ViewSet(CustomUpdateMixin, CustomCreateMixin, CustomDestroyMixin, viewsets.ModelViewSet):
#     queryset = discounts.objects.all()
#     serializer_class = discounts_Serializer
#     permission_classes = [IsAuthenticated]

# class inventory_adjustments_ViewSet(viewsets.ModelViewSet):
#     queryset = inventory_adjustments.objects.all()
#     serializer_class = inventory_adjustments_Serializer
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 data = serializer.validated_data
#                 item = data['item']
#                 quantity = data['quantity']
#                 adjustment_type = data['adjustment_type']
#                 reason = data.get('adjustment_reason', '')
#                 adjusted_by = data['adjusted_by']  

#                 # Validate adjustment type
#                 if adjustment_type not in ['Damage', 'Unsold_items']:
#                     return Response(
#                         {'error': 'Only Damage or Unsold_items adjustments are allowed'},
#                         status=400
#                     )

#                 # Check stock
#                 stock = stock_items.objects.get(item=item)
#                 if stock.quantity < quantity:
#                     return Response(
#                         {'error': f'Only {stock.quantity} items in stock. Cannot adjust {quantity}.'},
#                         status=400
#                     )

#                 # Create inventory adjustment
#                 inventory_adjustments.objects.create(
#                     item=item,
#                     quantity=quantity,
#                     adjustment_type=adjustment_type,
#                     adjustment_reason=reason,
#                     adjusted_by=adjusted_by,
#                     sales_order_return=None,
#                     created_at=timezone.now(),
#                     is_processed=False
#                 )

#                 # Update stock
#                 stock.quantity -= quantity
#                 stock.save()
#                 check_safety_stock(item)

#                 return Response({
#                     'status': "success",
#                     'message': f'{quantity} units of {item.item_name} removed from stock',
#                     'remaining_stock': stock.quantity
#                 }, status=201)

#             except stock_items.DoesNotExist:
#                 return Response({'error': 'Item not in stock'}, status=400)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=400)

#         return Response(serializer.errors, status=400)

    
# class items_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = items.objects.all()
#     serializer_class = items_Serializer
#     permission_classes = [IsAuthenticated]

# class sales_order_return_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = sales_order_return.objects.all()
#     serializer_class = sales_order_return_Serializer
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
    

# class purchase_order_return_ViewSet(viewsets.ModelViewSet):
#     queryset = purchase_order_return.objects.all()
#     serializer_class = purchase_order_return_Serializer
#     permission_classes = [IsAuthenticated]

#     @transaction.atomic
#     def create(self, request):
#         serializer = purchase_order_return_Serializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 data = serializer.validated_data
#                 adjustment_ids = data.get('adjustment_ids')
#                 created_by = request.user

#                 valid_adjustments = inventory_adjustments.objects.filter(
#                     id__in=adjustment_ids,
#                     adjustment_type__in=['Unsold_items', 'Damage'],
#                     is_processed=False
#                 )
                
#                 if valid_adjustments.count() != len(adjustment_ids):
#                     invalid_ids = set(adjustment_ids) - set(valid_adjustments.values_list('id', flat=True))
#                     return Response(
#                         {'error': f'Invalid or already processed adjustments: {invalid_ids}'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#                 total_refund = Decimal('0')
#                 return_items = []
#                 vendor = None

#                 for adj in valid_adjustments:
#                     try:
#                         po_detail = purchase_order_detail.objects.filter(
#                             item=adj.item
#                         ).order_by('-purchase_order__created_at').first()
                        
#                         if not po_detail:
#                             raise Exception(f"No purchase found for item {adj.item.id}")

#                         if not vendor:
#                             vendor = po_detail.purchase_order.vendor
#                         elif vendor != po_detail.purchase_order.vendor:
#                             return Response(
#                                 {'error': 'All items must belong to same vendor'},
#                                 status=status.HTTP_400_BAD_REQUEST
#                             )

#                         refund_amount = po_detail.price_per_piece * adj.quantity
#                         total_refund += refund_amount
#                         return_items.append({
#                             'item': adj.item,
#                             'quantity': adj.quantity,
#                             'price': po_detail.price_per_piece,
#                             'refund': refund_amount,
#                             'purchase_order': po_detail.purchase_order,
#                             'adjustment': adj
#                         })

#                     except Exception as e:
#                         return Response(
#                             {'error': str(e)},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )

#                 if not return_items:
#                     return Response(
#                         {'error': 'No valid items found for processing'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#                 # Create return header
#                 return_header = purchase_order_return.objects.create(
#                     purchase_orders=return_items[0]['purchase_order'],
#                     vendor=vendor,
#                     total_refund_amount=total_refund,
#                     created_at=timezone.now(),
#                     created_by=created_by
#                 )

#                 for item in return_items:
#                     # Create return detail
#                     purchase_order_return_detail.objects.create(
#                         return_purchase=return_header,
#                         purchase_order_detail=purchase_order_detail.objects.get(
#                             item=item['item'],
#                             purchase_order=item['purchase_order']
#                         ),
#                         return_quantity=item['quantity'],
#                         price_per_piece=item['price'],
#                         subtotal=item['refund'],
#                         created_at=timezone.now()
#                     )

#                     # Mark adjustment as processed
#                     item['adjustment'].is_processed = True
#                     item['adjustment'].save()

#                 # Process vendor refund using correct field
#                 self._process_vendor_refund(vendor, total_refund)

#                 return Response({
#                     'message': 'Purchase return processed successfully',
#                     'return_id': return_header.id,
#                     'total_refund': str(total_refund),
#                     'vendor_id': vendor.id,
#                     'vendor_name': vendor.vendor_name  
#                 }, status=status.HTTP_201_CREATED)

#             except Exception as e:
#                 return Response(
#                     {'error': str(e)},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def _process_vendor_refund(self, vendor, amount):
#         """Handle vendor refund processing using correct field"""
#         vendor.total_payables = (vendor.total_payables or Decimal('0')) - amount
#         vendor.save()        


    
# class purchase_order_return_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = purchase_order_return_detail.objects.all()
#     serializer_class = purchase_order_return_detail_Serializer
#     permission_classes = [IsAuthenticated]

    
# class purchase_order_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = purchase_order_detail.objects.all()
#     serializer_class = purchase_order_detail_Serializer
#     permission_classes = [IsAuthenticated]


# class purchase_receipts_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = purchase_receipts.objects.all()
#     serializer_class = purchase_receipts_Serializer
#     permission_classes = [IsAuthenticated]

# class sales_order_discounts_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = sales_order_discounts.objects.all()
#     serializer_class = sales_order_discounts_Serializer
#     permission_classes = [IsAuthenticated]

# class sales_orders_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = sales_orders.objects.all()
#     serializer_class = sale_orders_Serializer
#     permission_classes = [IsAuthenticated]
    
# class sales_order_return_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = sales_order_return_detail.objects.all()
#     serializer_class = sales_order_return_detail_Serializer
#     permission_classes = [IsAuthenticated]

# class sales_order_tax_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = sales_order_tax.objects.all()
#     serializer_class = sales_order_tax_Serializer
#     permission_classes = [IsAuthenticated]

    
# class shipments_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = shipments.objects.all()
#     serializer_class = shipments_Serializer
#     permission_classes = [IsAuthenticated]
    
# class stock_items_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = stock_items.objects.all()
#     serializer_class = stock_items_Serializer
#     permission_classes = [IsAuthenticated]
    
# class stockmanagement_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = stockmanagement.objects.all()
#     serializer_class = stockmanagement_Serializer
#     permission_classes = [IsAuthenticated]
    
# class tax_configurations_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = tax_configurations.objects.all()
#     serializer_class = tax_configurations_Serializer
#     permission_classes = [IsAuthenticated]
    
# class AuthUser_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = AuthUserSerializer
#     permission_classes = [IsAuthenticated]
    
# class vendors_ViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = vendors.objects.all()
#     serializer_class = vendors_Serializer
#     permission_classes = [IsAuthenticated]
    
# class warehouses_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
#     queryset = warehouses.objects.all()
#     serializer_class = warehouses_Serializer
#     permission_classes = [IsAuthenticated]
    
    
# class area_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = area.objects.all()
#     serializer_class = area_Serializer
#     permission_classes = [IsAuthenticated]
    
# class sales_order_detail_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
#     queryset = sales_order_detail.objects.all()
#     serializer_class = sales_order_detail_Serializer
#     permission_classes = [IsAuthenticated]
        

# def dashboard(request):
#     # Get counts and totals for dashboard cards
#     total_items = items.objects.count()
#     total_sales = sales_orders.objects.aggregate(
#         total=Sum('net_total')
#     )['total'] or 0
#     low_stock_items = stock_items.objects.filter(
#         quantity__lte=models.F('safety_stock_level')
#     ).count()
#     pending_orders = sales_orders.objects.filter(
#         order_status='Pending'
#     ).count()

#     # Get recent sales orders
#     recent_sales = sales_orders.objects.order_by('-created_at')[:5]

#     # Get low stock items
#     low_stock_list = stock_items.objects.filter(
#         quantity__lte=models.F('safety_stock_level')
#     ).select_related('item')[:5]

#     context = {
#         'total_items': total_items,
#         'total_sales': total_sales,
#         'low_stock_items': low_stock_items,
#         'pending_orders': pending_orders,
#         'recent_sales': recent_sales,
#         'low_stock_list': low_stock_list,
#     }
#     return render(request, 'dashboard.html', context)    


# For POS UI
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy





#Items Crud Views
class ItemListView(ListView):
    model = items
    template_name = 'items/item_list.html'
    context_object_name = 'items'

class ItemCreateView(CreateView):
    model = items
    fields = '__all__'
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item_list')

class ItemUpdateView(UpdateView):
    model = items
    fields = '__all__'
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item_list')

class ItemDeleteView(DeleteView):
    model = items
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')
    
#Categories Crud Views    
class CategoriesListView(ListView):
    model= categories
    template_name =  'categories/categories_list.html'
    context_object_name = 'categories'

class CategoriesUpdateView(UpdateView):
    model = categories
    fields = '__all__'
    template_name = "categories/categories_form.html"
    success_url = reverse_lazy('categories_list')
    
class CategoriesDeleteView(DeleteView):
    model = categories
    template_name = "categories/categories_delete.html"
    success_url = reverse_lazy('categories_list')
        
class CategoriesCreateView(CreateView):
    model = categories
    fields = '__all__'
    template_name = 'categories/categories_form.html'
    success_url = reverse_lazy('categories_list')    
    
    
# Customers Crud Views   
class customersListView(ListView):
    model = customers
    template_name = "customers/customers_list.html"
    context_object_name = 'customers'
    
class customersCreateView(CreateView):
    model = customers
    template_name = "customers/customers_form.html"
    fields = '__all__'
    success_url = reverse_lazy('customers_list')
    
class customersDeleteView(DeleteView):
    model = customers
    template_name = "customers/customers_delete.html"
    success_url = reverse_lazy('customers_list')
    
class customersUpdateView(UpdateView):
    model = customers
    template_name = "customers/customers_form.html"
    fields = '__all__'
    success_url = reverse_lazy('customers_list')
       
    
#Discount Crud Views   
class discountsListView(ListView):
    model = discounts
    template_name = "discounts/discounts_list.html"
    context_object_name = 'discounts'
    
class discountsCreateView(CreateView):
    model = discounts
    template_name = "discounts/discounts_form.html"
    fields = '__all__'
    success_url = reverse_lazy('discounts_list')
    
class discountsDeleteView(DeleteView):
    model = discounts
    template_name = "discounts/discounts_delete.html"
    success_url = reverse_lazy('discounts_list')
    
class discountsUpdateView(UpdateView):
    model = discounts
    template_name = "discounts/discounts_form.html"
    fields = '__all__'
    success_url = reverse_lazy('discounts_list')
     
#inventory_adjustments Crud Views
class inventory_adjustmentsListView(ListView):
    model = inventory_adjustments
    template_name = "inventory_adjustments/inventory_adjustments_list.html"
    context_object_name = 'inventory_adjustments'
    
class inventory_adjustmentsCreateView(CreateView):
    model = inventory_adjustments
    template_name = "inventory_adjustments/inventory_adjustments_form.html"
    fields = '__all__'
    success_url = reverse_lazy('inventory_adjustments_list')
    
class inventory_adjustmentsDeleteView(DeleteView):
    model = inventory_adjustments
    template_name = "inventory_adjustments/inventory_adjustments_delete.html"
    success_url = reverse_lazy('inventory_adjustments_list')
    
class inventory_adjustmentsUpdateView(UpdateView):
    model = inventory_adjustments
    template_name = "inventory_adjustments/inventory_adjustments_form.html"
    fields = '__all__'
    success_url = reverse_lazy('inventory_adjustments_list')
    
    
# Purchase_Orders Crud Views    
class purchase_ordersListView(ListView):
    model = purchase_orders
    template_name = "purchase_orders/purchase_orders_list.html"
    context_object_name = 'purchase_orders'
    
class purchase_ordersCreateView(CreateView):
    model = purchase_orders
    template_name = "purchase_orders/purchase_orders_form.html"
    fields = '__all__'
    success_url = reverse_lazy('purchase_orders_list')
    
class purchase_ordersDeleteView(DeleteView):
    model = purchase_orders
    template_name = "purchase_orders/purchase_orders_delete.html"
    success_url = reverse_lazy('purchase_orders_list')
    
class purchase_ordersUpdateView(UpdateView):
    model = purchase_orders
    template_name = "purchase_orders/purchase_orders_form.html"
    fields = '__all__'
    success_url = reverse_lazy('purchase_orders_list')
  
  
# Purchase Order Detail  Crud Views    
class purchase_order_detailListView(ListView):
    model = purchase_order_detail
    template_name = "purchase_order_detail/purchase_order_detail_list.html"
    context_object_name = 'purchase_order_detail'
    
class purchase_order_detailCreateView(CreateView):
    model = purchase_order_detail
    template_name = "purchase_order_detail/purchase_order_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy('purchase_order_detail_list')
    
class purchase_order_detailDeleteView(DeleteView):
    model = purchase_order_detail
    template_name = "purchase_order_detail/purchase_order_detail_delete.html"
    success_url = reverse_lazy('purchase_orders_detail_list')
    
class purchase_order_detailUpdateView(UpdateView):
    model = purchase_order_detail
    template_name = "purchase_order_detail/purchase_order_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy('purchase_order_detail_list')
  
# Purchase Order Return Crud Views
class purchase_order_returnListView(ListView):
    model = purchase_order_return
    template_name = "purchase_order_return/purchase_order_return_list.html"
    context_object_name = 'purchase_order_return'
    
class purchase_order_returnCreateView(CreateView):
    model = purchase_order_return
    template_name = "purchase_order_return/purchase_order_return_form.html"
    fields = '__all__'
    success_url = reverse_lazy('purchase_order_return_list')
        
class purchase_order_returnDeleteView(DeleteView):
    model = purchase_order_return
    template_name = "purchase_order_return/purchase_order_return_delete.html"
    success_url = reverse_lazy('purchase_order_return_list')
    
class purchase_order_returnUpdateView(UpdateView):
    model = purchase_order_return
    template_name = "purchase_order_return/purchase_order_return_form.html"
    fields = '__all__'
    success_url = reverse_lazy('purchase_order_return_list')

#Purchase Order Return Detail Crud Views
class purchase_order_return_detailListView(ListView):
    model = purchase_order_return_detail
    template_name = "purchase_order_return_detail/purchase_order_return_detail_list.html"
    context_object_name = 'purchase_order_return_detail'

class purchase_order_return_detailCreateView(CreateView):
    model = purchase_order_return_detail
    template_name = "purchase_order_return_detail/purchase_order_return_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy("purchase_order_return_detail_list")
    
class purchase_order_return_detailDeleteView(DeleteView):
    model = purchase_order_return_detail
    template_name = "purchase_order_return_detail/purchase_order_return_detail_delete.html"
    success_url = reverse_lazy("purchase_order_return_detail_list")
    
    
class purchase_order_return_detailUpdateView(UpdateView):
    model = purchase_order_return_detail
    template_name = "purchase_order_return_detail/purchase_order_return_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy("purchase_order_return_detail_list")


# Purchase Receipt Crud View
class purchase_receiptsListView(ListView):
    model = purchase_receipts
    template_name = "purchase_receipts/purchase_receipts_list.html"
    context_object_name = 'purchase_receipts'
    
class purchase_receiptsCreateView(CreateView):
    model = purchase_receipts
    template_name = "purchase_receipts/purchase_receipts_form.html"
    fields = '__all__'
    success_url = reverse_lazy("purchase_receipts_list")
    
class purchase_receiptsDeleteView(DeleteView):
    model = purchase_receipts
    template_name = "purchase_receipts/purchase_receipts_delete.html"
    success_url = reverse_lazy("purchase_receipts_list")
    
class purchase_receiptsUpdateView(UpdateView):
    model = purchase_receipts
    template_name = "purchase_receipts/purchase_receipts_form.html"
    fields = '__all__'
    success_url = reverse_lazy("purchase_receipts_list")
    
# Sales Order Discount Crud Views
class sales_order_discountsListView(ListView):
    model = sales_order_discounts
    template_name = "sales_order_discounts/sales_order_discounts_list.html"
    context_object_name = 'sales_order_discounts'
    
class sales_order_discountsCreateView(CreateView):
    model = sales_order_discounts
    template_name = "sales_order_discounts/sales_order_discounts_form.html"
    fields = '__all__'
    success_url = reverse_lazy("sales_order_discounts_list")
    
    
class sales_order_discountsDeleteView(DeleteView):
    model = sales_order_discounts
    template_name = "sales_order_discounts/sales_order_discounts_delete.html"
    success_url = reverse_lazy("sales_order_discounts_list")
    
class sales_order_discountsUpdateView(UpdateView):
    model = sales_order_discounts
    template_name = "sales_order_discounts/sales_order_discounts_form.html"
    fields = '__all__'
    success_url = reverse_lazy("sales_order_discounts_list")
    
#Area Crud Views
class areaListView(ListView):
    model = area
    template_name = "area/area_list.html"
    context_object_name = 'area'
    
    
class areaCreateView(CreateView):
    model = area
    template_name = "area/area_form.html"
    fields = '__all__'
    success_url = reverse_lazy('area_list')
    
class areaDeleteView(DeleteView):
    model = area
    template_name = "area/area_delete.html"
    success_url = reverse_lazy('area_list')

class areaUpdateView(UpdateView):
    model = area
    template_name = "area/area_form.html"
    fields = '__all__'
    success_url = reverse_lazy('area_list')
    
# Sales Orders Crud Views
class sales_ordersListView(ListView):
    model = sales_orders
    template_name = "sales_order/sales_orders_list.html"
    context_object_name = "sales_orders"
    
class sales_ordersCreateView(CreateView):
    model = sales_orders
    template_name = "sales_order/sales_orders_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_orders_list') 
    
class sales_ordersDeleteView(DeleteView):
    model = sales_orders
    template_name = "sales_order/sales_orders_delete.html"
    success_url = reverse_lazy('sales_orders_list')  
    
class sales_ordersUpdateView(UpdateView):
    model = sales_orders
    template_name = "sales_orders/sales_orders_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_orders_list')
    
    
#Sales Order Return Crud Views   
class sales_order_returnListView(ListView):
    model = sales_order_return
    template_name = "sales_order_return/sales_order_return_list.html"
    context_object_name = 'sales_order_return'
    
class sales_order_returnCreateView(CreateView):
    model = sales_order_return
    template_name = "sales_order_return/sales_order_return_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_order_return_list')
    
class sales_order_returnDeleteView(DeleteView):
    model = sales_order_return
    template_name = "sales_order_return/sales_order_return_delete.html"
    success_url = reverse_lazy('sales_order_return_list')
    
class sales_order_returnUpdateView(UpdateView):
    model = sales_order_return
    template_name = "sales_order_return/sales_order_return_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_order_return_list')
      
#Sales Order Return Detail Crud Views
class sales_order_return_detailListView(ListView):
    model = sales_order_return_detail
    template_name = "sales_order_return_detail/sales_order_return_detail_list.html"
    context_object_name = 'sales_order_return_detail'
    
class sales_order_return_detailCreateView(CreateView):
    model = sales_order_return_detail
    template_name = "sales_order_return_detail/sales_order_return_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy("sales_order_return_detail_list")

class sales_order_return_detailDeleteView(DeleteView):
    model = sales_order_return_detail
    template_name = "sales_order_return_detail/sales_order_return_detail_delete.html"
    success_url = reverse_lazy('sales_order_return_detail_list')
    
class sales_order_return_detailUpdateView(UpdateView):
    model = sales_order_return_detail
    template_name = "sales_order_return_detail/sales_order_return_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_order_return_detail_list')
    

# Sales Order Tax Crud Views
class sales_order_taxListView(ListView):
    model = sales_order_tax
    template_name = "sales_order_tax/sales_order_tax_list.html"
    context_object_name = 'sales_order_tax'
    
    
class sales_order_taxCreateView(CreateView):
    model = sales_order_tax
    template_name = "sales_order_tax/sales_order_tax_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_order_tax_list')
    
class sales_order_taxDeleteView(DeleteView):
    model = sales_order_tax
    template_name = "sales_order_tax/sales_order_tax_delete.html"
    success_url = reverse_lazy('sales_order_tax_list')
    
class sales_order_taxUpdateView(UpdateView):
    model = sales_order_tax
    template_name = "sales_order_tax/sales_order_tax_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_order_tax_list')    
    
    
#Shipment Crud Views
class shipmentsListView(ListView):
    model = shipments
    template_name = "shipments/shipments_list.html"
    context_object_name = 'shipments'
    
class shipmentsCreateView(CreateView):
    model = shipments
    template_name = "shipments/shipments_form.html"
    fields = '__all__'
    success_url = reverse_lazy('shipments_list')

class shipmentsUpdateView(CreateView):
    model = shipments
    template_name = "shipments/shipments_form.html"
    fields = '__all__'
    success_url = reverse_lazy("shipments_list")
    
class shipmentsDeleteView(DeleteView):
    model = shipments
    template_name = "shipments/shipments_delete.html"
    success_url = reverse_lazy('shipments_list')
    
#Stock Items Crud Views
class stock_itemsListView(ListView):
    model = stock_items
    template_name = "stock_items/stock_items_list.html"
    context_object_name = 'stock_items'
    
class stock_itemsCreateView(CreateView):
    model = stock_items
    template_name = "stock_items/stock_items_form.html"
    fields = '__all__'
    success_url = reverse_lazy('stock_items_list')
    
class stock_itemsDeleteView(DeleteView):
    model = stock_items
    template_name = "stock_items/stock_items_delete.html"
    success_url = reverse_lazy('stock_items_list')
    
class stock_itemsUpdateView(UpdateView):
    model = stock_items
    template_name = "stock_items/stock_items_form.html"
    fields = '__all__'
    success_url = reverse_lazy('stock_items_list')
    
# Stock Management Crud Views
class stockmanagementListView(ListView):
    model = stockmanagement
    template_name = "stockmanagement/stockmanagement_list.html"
    context_object_name = 'stockmanagement'
    
class stockmanagementCreateView(CreateView):
    model = stockmanagement
    template_name = "stockmanagement/stockmanagement_form.html"
    fields = '__all__'
    success_url = reverse_lazy("stockmanagement_list")
    
class stockmanagementDeleteView(DeleteView):
    model = stockmanagement
    template_name = "stockmanagement/stockmanagement_delete.html"
    success_url = reverse_lazy('stockmanagement_list')
    
class stockmanagementUpdateView(UpdateView):
    model = stockmanagement
    template_name = "stockmanagement/stockmanagement_form.html"
    fields = '__all__'
    success_url = reverse_lazy('stockmanagement_list')
 
 
#Tax Configurations Crud Views    
class tax_configurationsListView(ListView):
    model = tax_configurations
    template_name = "tax_configurations/tax_configurations_list.html"
    context_object_name = 'tax_configurations'
    
class tax_configurationsCreateView(CreateView):
    model = tax_configurations
    template_name = "tax_configurations/tax_configurations_form.html"
    fields = '__all__'
    success_url = reverse_lazy('tax_configurations_list')
    
class tax_configurationsDeleteView(DeleteView):
    model = tax_configurations
    template_name = "tax_configurations/tax_configurations_delete.html"
    success_url = reverse_lazy('tax_configurations_list')
    
class tax_configurationsUpdateView(UpdateView):
    model = tax_configurations
    template_name = "tax_configurations/tax_configurations_form.html"
    fields = '__all__'
    success_url = reverse_lazy('tax_configurations_list')
    
#Vendors Crud Views
class vendorsListView(ListView):
    model = vendors
    template_name = "vendors/vendors_list.html"
    context_object_name = 'vendors'
    
class vendorsCreateView(CreateView):
    model = vendors
    template_name = "vendors/vendors_form.html"
    fields = '__all__'
    success_url = reverse_lazy('vendors_list')


class vendorsUpdateView(UpdateView):
    model = vendors
    template_name = "vendors/vendors_form.html"
    fields = '__all__'
    success_url = reverse_lazy('vendors_list')
    
class vendorsDeleteView(DeleteView):
    model = vendors
    template_name = "vendors/vendors_delete.html"
    success_url = reverse_lazy('vendors_list')
    
# Warehouse Crud Views    
class warehousesListView(ListView):
    model = warehouses
    template_name = "warehouses/warehouses_list.html"
    context_object_name = 'warehouses'
    
class warehousesCreateView(CreateView):
    model = warehouses
    template_name = "warehouses/warehouses_form.html"
    fields = '__all__'
    success_url = reverse_lazy('warehouses_list')
    
class warehousesDeleteView(DeleteView):
    model = warehouses
    template_name = "warehouses/warehouses_delete.html"
    success_url = reverse_lazy('warehouses_list')
    
class warehousesUpdateView(UpdateView):
    model = warehouses
    template_name = "warehouses/warehouses_form.html"
    fields = '__all__'
    success_url = reverse_lazy('warehouses_list')
    
#Sales Order Detail Crud Views    
class sales_order_detailListView(ListView):
    model = sales_order_detail
    template_name = "sales_order_detail/sales_order_detail_list.html"
    context_object_name = 'sales_order_detail'
    
class sales_order_detailCreateView(CreateView):
    model = sales_order_detail
    template_name = "sales_order_detail/sales_order_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_order_detail_list')
    
class sales_order_detailUpdateView(UpdateView):
    model = sales_order_detail
    template_name = "sales_order_detail/sales_order_detail_form.html"
    fields = '__all__'
    success_url = reverse_lazy('sales_order_detail_list')
    
class sales_order_detailDeleteView(DeleteView):
    model = sales_order_detail
    template_name = "sales_order_detail/sales_order_detail_delete.html"
    success_url = reverse_lazy('sales_order_detail_list')

    
# Notification Crud Views
class notificationListView(ListView):
    model = notification
    template_name = "notification/notification_list.html"
    context_object_name = 'notification'
    
class notificationCreateView(CreateView):
    model = notification
    template_name = "notification/notification_form.html"
    fields = '__all__'
    success_url = reverse_lazy('notification_list')
    
class notificationUpdateView(UpdateView):
    model = notification
    template_name = "notification/notification_form.html"
    fields = '__all__'
    success_url = reverse_lazy('notification_list')
    
class notificationDeleteView(DeleteView):
    model = notification
    template_name = "notification/notification_delete.html"
    success_url = reverse_lazy('notification_list')



from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
import time

@transaction.atomic
def place_order(request):
    if request.method == 'GET':
        # Prepare data for the form
        context = {
            'customers': customers.objects.all(),
            'areas': area.objects.all(),
            'items': items.objects.all(),
            'discounts': discounts.objects.filter(is_active=True)
        }
        return render(request, 'orders/place_order.html', context)
    
    elif request.method == 'POST':
        try:
            # Get data from form submission
            customer_id = request.POST.get('customer_id')
            area_id = request.POST.get('area_id')
            
            # Parse order items from form
            order_details = []
            item_ids = request.POST.getlist('item_id')
            quantities = request.POST.getlist('quantity')
            discount_ids = request.POST.getlist('discount_id')
            
            for i in range(len(item_ids)):
                order_details.append({
                    'item_id': item_ids[i],
                    'quantity': quantities[i],
                    'discount_id': discount_ids[i] if i < len(discount_ids) else None
                })

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

                # Check stock
                stock_item = item.stock_items.first()
                if not stock_item:
                    raise ValidationError(f"Item {item.item_name} has no stock information")

                stock_quantity = int(stock_item.quantity)
                if stock_quantity < quantity:
                    raise ValidationError(f"Item {item.item_name} is out of stock")

                # Calculate prices
                price_per_piece = item.item_price
                discounted_price = price_per_piece
                
                # Apply discount if available
                if discount_id:
                    discount = discounts.objects.get(id=discount_id)
                    if discount and discount.is_active:
                        discounted_price = price_per_piece * (1 - discount.discount_percentage / 100)
                        total_discount += (price_per_piece - discounted_price) * quantity

                # Calculate tax
                tax_price = 0
                if item.tax:
                    tax_price = discounted_price * (item.tax.rate_percentage / 100)
                    total_tax += tax_price * quantity

                sub_total = (discounted_price + tax_price) * quantity
                total_amount += price_per_piece * quantity
                net_total += sub_total

                # Create order detail
                sales_order_detail.objects.create(
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

                # Update stock
                stock_item.quantity = stock_quantity - quantity
                stock_item.save()
                check_safety_stock(item)

            # Add delivery charges
            net_total += area_obj.delivery_charges

            # Update order totals
            sales_order.total_amount = total_amount
            sales_order.discount = total_discount
            sales_order.tax_amount = total_tax
            sales_order.net_total = net_total
            sales_order.save()

            # Update customer credit
            customer.total_bill = (customer.total_bill or Decimal('0')) + net_total
            if customer.credit_limit is not None and customer.total_bill > customer.credit_limit:
                raise ValidationError("Order exceeds customer's credit limit")
            customer.save()
            messages.success(request, 'Order placed successfully!')
            context = {
                'customers': customers.objects.all(),
                'areas': area.objects.all(),
                'items': items.objects.all(),
                'discounts': discounts.objects.filter(is_active=True)
            }
            return render(request, 'orders/place_order.html', context)

            # messages.success(request, 'Order placed successfully!')
            # return redirect('order_success', order_id=sales_orders.id)

        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            # Return form with previous data
            context = {
                'customers': customers.objects.all(),
                'areas': area.objects.all(),
                'items': items.objects.all(),
                'discounts': discounts.objects.filter(is_active=True),
                'error': str(e),
                'form_data': request.POST  
            }
            return render(request, 'orders/place_order.html', context)


def check_safety_stock(item):
        stock = stock_items.objects.get(item=item)
        if stock.quantity <= stock.safety_stock_level:
            # Check if notification already exists
            if not notification.objects.filter(item=item, is_read=False).exists():
                notification.objects.create(
                    item=item,
                    message=f"Stock for '{item.item_name}' has fallen below the safety level.",
                    created_at=timezone.now(),
                    is_read=False
                )
                # Optional: Send to WebSocket
                from asgiref.sync import async_to_sync
                from channels.layers import get_channel_layer
                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "notifications",  
                    {
                        "type": "send_notification",
                        "message": f"Restock '{item.item_name}'! Low stock alert."
                    }
                )

 
#Dashboard View
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total items
        context['total_items'] = items.objects.count()

        # Low stock items
        low_stock_items = items.objects.annotate(
            total_quantity=Sum('stock_items__quantity')
        ).filter(
            total_quantity__lte=F('safety_stock_level')
        )
        context['low_stock_count'] = low_stock_items.count()

        # Today's orders
        context['todays_orders'] = sales_orders.objects.filter(created_at__date=now().date()).count()

        # Notification count
        context['notification_count'] = notification.objects.count()

        # Recent alerts
        context['recent_alerts'] = notification.objects.order_by('-created_at')[:5]

        return context



# def order_success(request, order_id):
#     order = sales_orders.objects.get(id=order_id)
#     return render(request, 'order_success.html', {'order': order})


import json
from django.http import JsonResponse
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

class PurchaseOrderView(View):
    template_name = 'purchases/create_purchase_order.html'

    def get(self, request):
        context = {
            'vendors': vendors.objects.all(),
            'items': items.objects.all(),
            'categories': categories.objects.all(),
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        try:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)

            vendor_id = data.get('vendor_id')
            order_details = data.get('order_details', [])

            if not vendor_id:
                raise ValueError("Vendor ID is required")
            
            if not order_details:
                raise ValueError("At least one order item is required")


            vendor = vendors.objects.get(id=vendor_id)

            total_amount = Decimal('0')
            total_discount = Decimal('0')
            total_tax = Decimal('0')
            net_total = Decimal('0')

            # Create purchase order
            purchase_order = purchase_orders.objects.create(
                purchase_order_number=f"PO{vendor_id}{int(time.time())}",
                vendor=vendor,
                order_status='Pending',
                total_amount=0,
                discount=0,
                tax_amount=0,
                net_total=0,
                created_at=timezone.now()
            )

            for detail in order_details:
                # Validate required fields
                if not detail.get('item_id') or not detail.get('quantity') or not detail.get('price_per_piece'):
                    raise ValueError("Item ID, quantity, and price are required for all items")

                item_id = detail.get('item_id')
                item_name = detail.get('item_name', f"Item-{item_id}")
                quantity = int(detail.get('quantity'))
                price_per_piece = Decimal(str(detail.get('price_per_piece')))
                discount_percentage = Decimal(str(detail.get('discount_percentage', 0)))
                tax_percentage = Decimal(str(detail.get('tax_percentage', 0)))
                category_name = detail.get('category_name', 'Uncategorized')

                # Create or get item
                item, item_created = items.objects.get_or_create(
                    id=item_id,
                    defaults={
                        'item_name': item_name,
                        'item_code': f"ITEM-{item_id}",
                        'sku': f"SKU-{item_id}",
                        'item_price': price_per_piece,
                        'item_type': 'Good',
                        'created_at': timezone.now()
                    }
                )

                # Create or get category
                category, _ = categories.objects.get_or_create(
                    category_name=category_name,
                    defaults={
                        'category_desc': f"Auto-created for {item_name}",
                        'created_at': timezone.now()
                    }
                )

                if item_created:
                    item.category = category
                    item.save()

                # Calculate amounts
                item_total = price_per_piece * quantity
                discount_amount = item_total * (discount_percentage / Decimal('100'))
                discounted_price = item_total - discount_amount
                tax_amount = discounted_price * (tax_percentage / Decimal('100'))
                sub_total = discounted_price + tax_amount

                total_amount += item_total
                total_discount += discount_amount
                total_tax += tax_amount
                net_total += sub_total

                # Create order detail
                purchase_order_detail.objects.create(
                    item=item,
                    purchase_order=purchase_order,
                    quantity=quantity,
                    price_per_piece=price_per_piece,
                    discounted_price=discounted_price / quantity,
                    price_after_discount=discounted_price,
                    tax_price=tax_amount,
                    price_after_tax=sub_total,
                    sub_total=sub_total
                )

                # Update stock if it's a good item
                if item.item_type == 'Good':
                    stock_item, created = stock_items.objects.get_or_create(
                        item=item,
                        defaults={
                            'quantity': quantity,
                            'safety_stock_level': 10,
                            'last_restocked_at': timezone.now()
                        }
                    )
                    if not created:
                        stock_item.quantity += quantity
                        stock_item.last_restocked_at = timezone.now()
                        stock_item.save()

            # Update purchase order totals
            purchase_order.total_amount = total_amount
            purchase_order.discount = total_discount
            purchase_order.tax_amount = total_tax
            purchase_order.net_total = net_total
            purchase_order.save()

            return JsonResponse({
                'success': True,
                'message': 'Purchase order created successfully',
                'order_number': purchase_order.purchase_order_number
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        
# class PurchaseOrderView(View):
#     template_name = 'purchases/create_purchase_order.html'

#     def get(self, request):
#         context = {
#             'vendors': vendors.objects.all(),
#             'items': items.objects.all(),
#         }
#         return render(request, self.template_name, context)

#     @transaction.atomic
#     def post(self, request):
#         try:
#             vendor_id = request.POST.get('vendor_id')
#             order_details = request.POST.getlist('order_details')  

#             vendor = vendors.objects.get(id=vendor_id)

#             total_amount = Decimal('0')
#             total_discount = Decimal('0')
#             total_tax = Decimal('0')
#             net_total = Decimal('0')

#             purchase_order = purchase_orders.objects.create(
#                 purchase_order_number=f"PO{vendor_id}{int(time.time())}",
#                 vendor=vendor,
#                 order_status='Pending',
#                 total_amount=0,
#                 discount=0,
#                 tax_amount=0,
#                 net_total=0,
#                 created_at=timezone.now()
#             )

#             for detail in order_details:
#                 item_id = detail.get('item_id')
#                 item_name = detail.get('item_name', f"Item-{item_id}")
#                 quantity = int(detail.get('quantity'))
#                 price_per_piece = Decimal(str(detail.get('price_per_piece')))
#                 discount_percentage = Decimal(str(detail.get('discount_percentage', 0)))
#                 tax_percentage = Decimal(str(detail.get('tax_percentage', 0)))
#                 category_name = detail.get('category_name', 'Uncategorized')

#                 item, item_created = items.objects.get_or_create(
#                     id=item_id,
#                     defaults={
#                         'item_name': item_name,
#                         'item_code': f"ITEM-{item_id}",
#                         'sku': f"SKU-{item_id}",
#                         'item_price': price_per_piece,
#                         'item_type': 'Good',
#                         'created_at': timezone.now()
#                     }
#                 )

#                 category, _ = categories.objects.get_or_create(
#                     category_name=category_name,
#                     defaults={
#                         'category_desc': f"Auto-created for {item_name}",
#                         'created_at': timezone.now()
#                     }
#                 )

#                 if item_created:
#                     item.category = category
#                     item.save()

#                 item_total = price_per_piece * quantity
#                 discount_amount = item_total * (discount_percentage / Decimal('100'))
#                 discounted_price = item_total - discount_amount
#                 tax_amount = discounted_price * (tax_percentage / Decimal('100'))
#                 sub_total = discounted_price + tax_amount

#                 total_amount += item_total
#                 total_discount += discount_amount
#                 total_tax += tax_amount
#                 net_total += sub_total

#                 purchase_order_detail.objects.create(
#                     item=item,
#                     purchase_order=purchase_order,
#                     quantity=quantity,
#                     price_per_piece=price_per_piece,
#                     discounted_price=discounted_price / quantity,
#                     price_after_discount=discounted_price,
#                     tax_price=tax_amount,
#                     price_after_tax=sub_total,
#                     sub_total=sub_total
#                 )

#                 if item.item_type == 'Good':
#                     stock_item, created = stock_items.objects.get_or_create(
#                         item=item,
#                         defaults={
#                             'quantity': quantity,
#                             'safety_stock_level': 10,
#                             'last_restocked_at': timezone.now()
#                         }
#                     )
#                     if not created:
#                         stock_item.quantity += quantity
#                         stock_item.last_restocked_at = timezone.now()
#                         stock_item.save()

#             purchase_order.total_amount = total_amount
#             purchase_order.discount = total_discount
#             purchase_order.tax_amount = total_tax
#             purchase_order.net_total = net_total
#             purchase_order.save()

#             messages.success(request, "Purchase order created successfully.")
#             return redirect('purchase_order_success') 
#         except Exception as e:
#             messages.error(request, f"Error: {str(e)}")
#             return redirect('create_purchase_order') 
    
    
# class ProcessReturnView(View):
#     def post(self, request):
#         data = request.POST

#         try:
#             return_details = request.POST.getlist('return_details')
#             # If return_details is sent as JSON string (from frontend), parse it
#             import json
#             return_details = json.loads(return_details[0]) if return_details else []
#         except Exception:
#             return HttpResponseBadRequest("Invalid return_details format.")

#         with transaction.atomic():
#             try:
#                 required_fields = ['sales_order_id', 'return_reason', 'return_type', 'created_by']
#                 for field in required_fields:
#                     if field not in data:
#                         return HttpResponseBadRequest(f"Missing field: {field}")

#                 return_type = data['return_type']
#                 if return_type not in ['return', 'damage', 'loss']:
#                     return HttpResponseBadRequest("Invalid return_type.")

#                 try:
#                     created_by = User.objects.get(id=data['created_by'])
#                 except User.DoesNotExist:
#                     return HttpResponseBadRequest("Invalid created_by user ID")

#                 try:
#                     sales_order = sales_orders.objects.get(id=data['sales_order_id'])
#                 except sales_orders.DoesNotExist:
#                     return HttpResponseBadRequest("Sales Order not found")

#                 sales_detail_id = return_details[0]['sales_order_detail_id']
#                 try:
#                     sales_detail = sales_order_detail.objects.get(id=sales_detail_id, sales_order=sales_order)
#                 except sales_order_detail.DoesNotExist:
#                     return HttpResponseBadRequest(f"Order detail {sales_detail_id} not found")

#                 return_header = sales_order_return.objects.create(
#                     sales_order=sales_order,
#                     customer=sales_order.customer,
#                     total_refund_amount=0,
#                     sales_order_detail=sales_detail,
#                     return_type=return_type,
#                     return_reason=data['return_reason'],
#                     created_at=timezone.now(),
#                     created_by=created_by
#                 )

#                 total_refund = Decimal('0')

#                 for detail in return_details:
#                     try:
#                         order_detail = sales_order_detail.objects.get(
#                             id=detail['sales_order_detail_id'],
#                             sales_order=sales_order
#                         )
#                     except sales_order_detail.DoesNotExist:
#                         return HttpResponseBadRequest(f"Detail {detail['sales_order_detail_id']} not found")

#                     if detail['return_quantity'] > order_detail.quantity:
#                         return HttpResponseBadRequest(
#                             f"Return quantity exceeds ordered quantity for item {order_detail.item.item_name}"
#                         )

#                     return_qty = Decimal(str(detail['return_quantity']))
#                     price = Decimal(str(order_detail.price_per_piece))
#                     refund_amount = price * return_qty
#                     total_refund += refund_amount

#                     sales_order_return_detail.objects.create(
#                         return_sale=return_header,
#                         sales_order_detail=order_detail,
#                         item=order_detail.item,
#                         return_quantity=int(return_qty),
#                         price_per_piece=price,
#                         subtotal=refund_amount,
#                         created_at=timezone.now()
#                     )

#                     if return_type == 'return':
#                         stock_item, _ = stock_items.objects.get_or_create(item=order_detail.item)
#                         stock_item.quantity += int(return_qty)
#                         stock_item.save()

#                     inventory_adjustments.objects.create(
#                         item=order_detail.item,
#                         sales_order_return=return_header,
#                         adjustment_type=return_type,
#                         quantity=int(return_qty),
#                         adjustment_reason=data['return_reason'],
#                         created_at=timezone.now(),
#                         adjusted_by=created_by
#                     )

#                 return_header.total_refund_amount = total_refund
#                 return_header.save()

#                 if return_type == 'return':
#                     customer = sales_order.customer
#                     customer.total_bill = (customer.total_bill or Decimal('0')) - total_refund
#                     customer.save()

#                 return redirect('success_page') 
#             except Exception as e:
#                 return HttpResponseBadRequest(f"Return processing failed: {str(e)}")

#     def get(self, request):
#         return render(request, 'process_return.html')  
