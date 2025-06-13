from rest_framework import viewsets,mixins,status
from .models import categories,vendor_bill, warehouse_stock, vendor_transfer_note, store,request_note, request_note_detail, receive_note, receive_note_detail, transfer_note, transfer_note_detail, sales_order_return,sales_order_return_detail,notification, purchase_order_return_detail, sales_order_detail, purchase_order_return, area,purchase_order_detail, customers, discounts, inventory_adjustments, items, purchase_orders, purchase_receipts, Custom_User, sales_order_discounts, sales_orders, sales_order_tax,shipments, stock_items, tax_configurations,  vendors, warehouses
from .serializers import SalesReportSerializer,vendor_transfer_note_detail, vendor_bill_Serializer,vendor_transfer_note_detail_Serializer,vendor_transfer_note_Serializer , receive_note_detail_Serializer, request_note_detail_Serializer,  warehouse_stock_Serializer, request_note_Serializer, transfer_note_detail_Serializer, transfer_note_Serializer, receive_note_Serializer, store_Serializer, CustomTokenRefreshSerializer, categories_Serializer, sales_order_return_Serializer,notification_Serializer, sales_order_return_detail_Serializer, purchase_order_return_detail_Serializer,purchase_order_return_Serializer,purchase_order_detail_Serializer, sales_order_detail_Serializer, place_order_Serializer,area_Serializer, customers_Serializer, discounts_Serializer, inventory_adjustments_Serializer, items_Serializer, purchase_orders_Serializer, purchase_receipts_Serializer, sales_order_discounts_Serializer, sale_orders_Serializer, sales_order_tax_Serializer, shipments_Serializer, stock_items_Serializer, tax_configurations_Serializer, AuthUserSerializer, vendors_Serializer, warehouses_Serializer
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from django.shortcuts import render, get_object_or_404
from channels.layers import get_channel_layer
from decimal import Decimal
from django.shortcuts import render, redirect
from django.db import transaction
import time
from django.db.models import Sum, Count, F


class vendor_bill_ViewSet(viewsets.ModelViewSet):
    queryset = vendor_bill.objects.all()
    serializer_class = vendor_bill_Serializer
    permission_classes = [IsAuthenticated]
    
class vendor_transfer_note_detail_ViewSet(viewsets.ModelViewSet):
    queryset = vendor_transfer_note_detail.objects.all()
    serializer_class = vendor_transfer_note_detail_Serializer  
    permission_classes = [IsAuthenticated]
    
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from decimal import Decimal
from django.utils import timezone

class vendor_transfer_note_ViewSet(viewsets.ModelViewSet):
    queryset = vendor_transfer_note.objects.all()
    serializer_class = vendor_transfer_note_Serializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            result = create_vendor_transfer_note_api(request.data, request.user)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'errors': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_vendor_transfer_note_api(request_data, user):
    with transaction.atomic():
        try:
            # 1. Validate Required Fields
            required_fields = {
                'vendor_transfer_note_no': "Transfer note number is required",
                'purchase_order': "Purchase order is required",
                'vendor': "Vendor is required",
                'items': "At least one item is required"
            }
            
            errors = {}
            for field, error_msg in required_fields.items():
                if field not in request_data or not request_data[field]:
                    errors[field] = [error_msg]
            
            if errors:
                raise ValueError(errors)
            
            if not isinstance(request_data['items'], list) or len(request_data['items']) == 0:
                raise ValueError({"items": ["At least one item must be provided"]})

            # 2. Get Related Objects
            try:
                purchase_order = purchase_orders.objects.select_related('warehouse').get(id=request_data['purchase_order'])
                if not purchase_order.warehouse:
                    raise ValueError({"purchase_order": ["Purchase order has no warehouse assigned"]})
                warehouse = purchase_order.warehouse
            except purchase_orders.DoesNotExist:
                raise ValueError({"purchase_order": ["Invalid purchase order ID"]})

            try:
                vendor = vendors.objects.get(id=request_data['vendor'])
            except vendors.DoesNotExist:
                raise ValueError({"vendor": ["Invalid vendor ID"]})

            # 3. Create Transfer Note with warehouse from PO
            transfer_note = vendor_transfer_note.objects.create(
                vendor_transfer_note_no=request_data['vendor_transfer_note_no'],
                purchase_order=purchase_order,
                warehouse=warehouse,  # This is now guaranteed to exist
                status=request_data.get('status', 'dispatched'),
                remarks=request_data.get('remarks', ''),
                vendor=vendor,
                # created_by=user
            )

            # 4. Process Items and Calculate Total
            total_amount = Decimal('0')
            for item_data in request_data['items']:
                try:
                    item = items.objects.get(id=item_data['item_id'])
                except items.DoesNotExist:
                    raise ValueError({"items": [f"Item {item_data.get('item_id')} does not exist"]})

                try:
                    quantity = int(item_data['quantity'])
                    price_per_piece = Decimal(str(item_data['price_per_piece']))
                except (KeyError, ValueError) as e:
                    raise ValueError({"items": ["Each item must have valid quantity and price_per_piece"]})

                # Create Transfer Note Detail
                vendor_transfer_note_detail.objects.create(
                    vendor_transfer_note=transfer_note,
                    item=item,
                    price_per_piece=price_per_piece,
                    quantity=quantity,
                    # created_at=timezone.now()
                )
                total_amount += price_per_piece * quantity

            # 5. Automatically Generate Vendor Bill
            # tax_amount = total_amount * Decimal('0.05')  # 5% tax
            bill = vendor_bill.objects.create(
                bill_number=f"BILL-{transfer_note.id}-{timezone.now().strftime('%Y%m%d')}",
                vendor_transfer_note=transfer_note,
                # vendor=vendor,
                # total_amount=total_amount,
                # tax_amount=tax_amount,
                # discount=Decimal('0.00'),
                net_amount=total_amount ,
                due_date=timezone.now() + timezone.timedelta(days=30),
                status='pending',
                created_at=timezone.now(),
                # created_by=user
            )

            return {
                'status': 'success',
                'message': 'Transfer Note Created Successfully',
                # 'transfer_note': {
                #     'id': transfer_note.id,
                #     'note_number': transfer_note.vendor_transfer_note_no,
                #     'warehouse_id': warehouse.id,
                #     'warehouse_name': warehouse.warehouse_name,
                #     'purchase_order': purchase_order.purchase_order_number
                # },
                # 'bill': {
                #     'id': bill.id,
                #     'bill_number': bill.bill_number,
                #     'net_amount': float(bill.net_amount)
                # },
                # 'items_processed': len(request_data['items'])
            }

        except ValueError as ve:
            if isinstance(ve.args[0], dict):
                raise ValueError(ve.args[0])
            raise ValueError({"error": [str(ve)]})
        except Exception as e:
            raise ValueError({"error": [f"An unexpected error occurred: {str(e)}"]})
                                
class purchaseordersViewSet(viewsets.ModelViewSet):
    queryset = purchase_orders.objects.all()
    serializer_class = purchase_orders_Serializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        # Check if user is linked to a warehouse
        if not user.warehouse:
            return Response({"error": "User is not assigned to any warehouse."}, status=status.HTTP_400_BAD_REQUEST)

        vendor_id = request.data.get("vendor_id")
        remarks = request.data.get("remarks")
        order_details = request.data.get("order_details")
        

        if not order_details:
            return Response({"error": "Order details are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create Purchase Order
            po = purchase_orders.objects.create(
                purchase_order_number=f"PO-{timezone.now().strftime('%Y%m%d%H%M%S')}",  # Auto-generate
                vendor_id=vendor_id,
                warehouse=user.warehouse,
                created_by=user,
                status='pending',
                created_at = timezone.now(),
                remarks =remarks
            )

            # Add each item detail
            for detail in order_details:
                item_id = detail.get("item_id")
                quantity = detail.get("quantity")
                
                if not item_id or not quantity:
                    continue  

                purchase_order_detail.objects.create(
                    purchase_order=po,
                    item_id=item_id,
                    quantity=quantity,
                    created_at=timezone.now()
                )

            serializer = self.get_serializer(po)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response({
                    'status' : 'success',
                    'message': 'Order placed successfully',
                    
                }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def process_return(request_data, user):
    with transaction.atomic():
        try:
            # 1. Validate Input Data
            required_fields = ['sales_order_id', 'return_details', 'return_reason', 'return_type', 'created_by']
            for field in required_fields:
                if field not in request_data:
                    raise ValueError(f"Missing required field: {field}")

            valid_return_types = ['return', 'damage', 'loss']
            if request_data['return_type'] not in valid_return_types:
                raise ValueError(f"Invalid return type. Must be one of: {', '.join(valid_return_types)}")

            try:
                create_by_user = Custom_User.objects.get(id=request_data['created_by'])
            except Custom_User.DoesNotExist:
                raise ValueError(f"User with ID {request_data['created_by']} does not exist")
                    
            # 2. Verify Sales Order exists
            try:
                sales_order = sales_orders.objects.get(id=request_data['sales_order_id'])
            except sales_orders.DoesNotExist:
                raise ValueError(f"Sales Order {request_data['sales_order_id']} does not exist")
            
            # Verify Sales order detail 
            sales_detail_id = request_data['return_details'][0]['sales_order_detail_id']
            try:
                sales_detail = sales_order_detail.objects.get(
                    id=sales_detail_id,
                    sales_order=sales_order
                )
            except sales_order_detail.DoesNotExist:
                raise ValueError(f"Order detail {sales_detail_id} not found in order {request_data['sales_order_id']}")

            # 3. Create Return Header with return_type
            return_header = sales_order_return.objects.create(
                sales_order=sales_order,
                customer=sales_order.customer,
                total_refund_amount=0,
                sales_order_detail=sales_detail,
                return_type=request_data['return_type'],  
                return_reason=request_data['return_reason'],  
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

                # Create inventory adjustment with the same return_type
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


class purchase_order_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = purchase_order_detail.objects.all()
    serializer_class = purchase_order_detail_Serializer
    permission_classes = [IsAuthenticated]
    
class notification_ViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = notification.objects.all()
    serializer_class = notification_Serializer
    permission_classes = [IsAuthenticated]

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

class PlaceOrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request):
        serializer = place_order_Serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                customer_id = data.get('customer_id')
                area_id = data.get('area_id')  
                order_details = data.get('order_details')
                
                # Get the current user and their store
                current_user = request.user
                if not hasattr(current_user, 'store') or not current_user.store:
                    raise ValidationError("User is not associated with any store")
                store = current_user.store  # The store associated with logged-in user

                # Validate customer
                try:
                    customer = customers.objects.get(id=customer_id)
                    if customer.credit_limit is None:
                        customer.credit_limit = Decimal('0')
                except customers.DoesNotExist:
                    raise ValidationError("Customer not found")        
                                
                # Validate area if provided
                area_obj = None
                if area_id:
                    area_obj = area.objects.get(id=area_id)

                # Initialize order totals
                total_amount = Decimal('0')
                total_discount = Decimal('0')
                total_tax = Decimal('0')
                net_total = Decimal('0')

                # Create sales order (not saved yet)
                sales_order = sales_orders(
                    sales_order_number=f"SO{customer_id}{int(time.time())}", 
                    customer=customer,
                    area=area_obj,
                    order_status='Delivered',
                    total_amount=Decimal('0'),  
                    discount=Decimal('0'),  
                    tax_amount=Decimal('0'),  
                    net_total=Decimal('0'),
                    store=store,    
                    created_at=timezone.now()
                )

                # Process each item in the order
                order_items = []
                for item_detail in order_details:
                    item_id = item_detail.get('item_id')
                    quantity = Decimal(item_detail.get('quantity'))
                    discount_id = item_detail.get('discount_id')
                    tax_id = item_detail.get('tax_id') 

                    # Validate item exists
                    item = items.objects.get(id=item_id)

                    # Get stock ONLY from the user's associated store
                    try:
                        stock_item = stock_items.objects.select_for_update().get(
                            item=item, 
                            store=store  # Only check stock in user's store
                        )
                    except stock_items.DoesNotExist:
                        raise ValidationError(f"Item {item.item_name} is not available in your store ({store.store_name})")

                    # Check stock availability
                    if stock_item.quantity < quantity:
                        raise ValidationError(
                            f"Insufficient stock for {item.item_name} in your store. "
                            f"Available: {stock_item.quantity}, Requested: {quantity}"
                        )

                    # Calculate pricing
                    price_per_piece = item.item_price
                    discounted_price = price_per_piece
                    
                    # Apply discount if provided
                    if discount_id:
                        discount = discounts.objects.get(id=discount_id)
                        if discount and discount.is_active:
                            discounted_price = price_per_piece * (1 - discount.discount_percentage / Decimal('100'))
                            total_discount += (price_per_piece - discounted_price) * quantity

                    # Apply tax
                    tax_price = Decimal('0')
                    if tax_id:
                        tax_config = tax_configurations.objects.get(id=tax_id)
                        if tax_config.applies_to in ['Sales', 'Both']:
                            tax_price = discounted_price * (tax_config.rate_percentage / Decimal('100'))
                    elif item.tax:
                        tax_price = discounted_price * (item.tax.rate_percentage / Decimal('100'))
                    
                    total_tax += tax_price * quantity
                    sub_total = (discounted_price + tax_price) * quantity

                    # Update totals
                    total_amount += price_per_piece * quantity
                    net_total += sub_total

                    # Prepare order item data
                    order_items.append({
                        'item': item,
                        'quantity': quantity,
                        'stock_item': stock_item,
                        'price_data': {
                            'price_per_piece': price_per_piece,
                            'discounted_price': discounted_price,
                            'tax_price': tax_price,
                            'sub_total': sub_total
                        }
                    })

                # Add delivery charges if area is specified
                if area_obj:
                    net_total += area_obj.delivery_charges

                # Check credit limit
                if customer.total_bill + net_total > customer.credit_limit:
                    raise ValidationError(
                        f"Order exceeds customer's credit limit. "
                        f"Current bill: {customer.total_bill}, Credit limit: {customer.credit_limit}"
                    )

                # Save the sales order with final totals
                sales_order.total_amount = total_amount
                sales_order.discount = total_discount
                sales_order.tax_amount = total_tax
                sales_order.net_total = net_total
                sales_order.save()

                # Process order items and update stock
                for item_data in order_items:
                    # Create order detail record
                    sales_order_detail.objects.create(
                        sales_order=sales_order,
                        item=item_data['item'],
                        quantity=item_data['quantity'],
                        price_per_piece=item_data['price_data']['price_per_piece'],
                        discounted_price=item_data['price_data']['discounted_price'],
                        price_after_discount=item_data['price_data']['discounted_price'],
                        tax_price=item_data['price_data']['tax_price'],
                        price_after_tax=item_data['price_data']['discounted_price'] + item_data['price_data']['tax_price'],
                        sub_total=item_data['price_data']['sub_total']
                    )

                    # Update stock in the user's store ONLY
                    stock_item = item_data['stock_item']
                    stock_item.quantity = F('quantity') - item_data['quantity']
                    stock_item.save()

                    # Check for safety stock level
                    stock_item.refresh_from_db()
                    if (stock_item.safety_stock_level is not None and 
                        stock_item.quantity <= stock_item.safety_stock_level):
                        # Create notification
                        notification.objects.create(
                            item_choices='store',
                            message=f"{item_data['item'].item_name} reached safety stock in {store.store_name}",
                            item=item_data['item'],
                            store=store
                        )

                        # Create request note to warehouse
                        request_note_instance = request_note.objects.create(
                            store=store,
                            status='approved',
                            remarks=f"Auto-generated request due to safety stock level reached for item {item_data['item'].item_name}",
                            created_at=timezone.now(),
                            created_by = current_user
                        )

                        # Create request note detail to warehouse
                        request_note_detail_obj = request_note_detail(
                            item=item_data['item'],
                            quantity=stock_item.safety_stock_level * 5,
                            request_note=request_note_instance                            
                        )
                        request_note_detail_obj.save()

                # Update customer's total bill
                customer.total_bill = F('total_bill') + net_total
                customer.save()

                return Response({
                    'message': 'Order placed successfully',
                    'order_id': sales_order.id,
                    'store': store.store_name  
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
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
    
def categories_list_view(request):
    all_categories = categories.objects.all()
    return render(request, 'categories_list.html', {'categories': all_categories})
    

class customers_ViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = customers.objects.all()
    serializer_class = customers_Serializer
    permission_classes = [IsAuthenticated]

class discounts_ViewSet(CustomUpdateMixin, CustomCreateMixin, CustomDestroyMixin, viewsets.ModelViewSet):
    queryset = discounts.objects.all()
    serializer_class = discounts_Serializer
    permission_classes = [IsAuthenticated]

class store_ViewSet(CustomCreateMixin, CustomDestroyMixin, CustomUpdateMixin, viewsets.ModelViewSet):
    queryset = store.objects.all()
    serializer_class = store_Serializer
    permission_classes = [IsAuthenticated]
        
class request_note_detail_ViewSet(CustomCreateMixin, CustomDestroyMixin, CustomUpdateMixin, viewsets.ModelViewSet):
    queryset= request_note_detail.objects.all()
    serializer_class = request_note_detail_Serializer
    permission_classes = [IsAuthenticated]    
    
class request_note_ViewSet(CustomCreateMixin, CustomDestroyMixin, CustomUpdateMixin, viewsets.ModelViewSet):
    queryset= request_note.objects.all()
    serializer_class = request_note_Serializer
    permission_classes = [IsAuthenticated]    


class transfer_note_detail_ViewSet(CustomCreateMixin, CustomUpdateMixin, CustomDestroyMixin, viewsets.ViewSet):
    queryset = transfer_note_detail.objects.all()
    serializer_class = transfer_note_detail_Serializer
    permission_classes= [IsAuthenticated]


class transfer_note_ViewSet(CustomCreateMixin, CustomDestroyMixin, CustomUpdateMixin, viewsets.ModelViewSet):
    queryset = transfer_note.objects.all()
    serializer_class = transfer_note_Serializer
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            current_user = request.user
            if not hasattr(current_user, 'warehouse') or not current_user.warehouse:
                raise ValidationError("User is not associated with any warehouse")
            
            warehouse = current_user.warehouse
            items_data = request.data.get('items', [])
            remarks = request.data.get('remarks', '')

            # Validate request note if provided
            request_note_obj = None
            request_note_id = request.data.get('request_note_id')
            if request_note_id:
                try:
                    request_note_obj = request_note.objects.select_related('store').get(id=request_note_id)
                except request_note.DoesNotExist:
                    raise ValidationError(f"Request note {request_note_id} not found")

            # Require items_data in all cases (ignore request_note_detail quantities)
            if not items_data:
                raise ValidationError("Items with quantities must be explicitly provided in the request")

            # Create the transfer note
            transfer_note_obj = transfer_note.objects.create(
                request_note=request_note_obj,
                warehouse_id=warehouse.id,  
                transferred_by_id=current_user.id,  
                remarks=remarks,
                status='dispatched'
            )

            # Process items from request payload (ignore request_note_detail)
            for item_data in items_data:
                item_id = item_data.get('item_id')
                quantity = int(item_data.get('quantity', 0))
                
                if quantity <= 0:
                    raise ValidationError(f"Quantity must be positive for item {item_id}")

                try:
                    item = items.objects.get(id=item_id)
                    stock = warehouse_stock.objects.select_for_update().get(
                        warehouse=warehouse, 
                        item=item
                    )
                    
                    if stock.quantity < quantity:
                        raise ValidationError(
                            f"Insufficient stock for {item.item_name} "
                            f"(Available: {stock.quantity}, Requested: {quantity})"
                        )

                    # Create transfer detail
                    transfer_note_detail.objects.create(
                        item=item,
                        transfer_note=transfer_note_obj,
                        quantity=quantity,  
                    )

                    # Update stock
                    stock.quantity = F('quantity') - quantity
                    stock.save()
                    stock.refresh_from_db()

                    # Safety stock check
                    if (stock.safety_stock_level is not None and 
                        stock.quantity <= stock.safety_stock_level):
                        notification.objects.create(
                            item_choices='warehouse',
                            message=f"{item.item_name} reached safety stock in {warehouse.warehouse_name}",
                            item=item,
                            warehouse=warehouse
                        )

                except items.DoesNotExist:
                    raise ValidationError(f"Item {item_id} not found")
                except warehouse_stock.DoesNotExist:
                    raise ValidationError(f"Item {item_id} not available in warehouse")

            return Response({
                'message': 'Transfer note created successfully',
                'transfer_note_id': transfer_note_obj.id,
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class receive_note_ViewSet(CustomCreateMixin, CustomUpdateMixin, CustomDestroyMixin, viewsets.ModelViewSet):
    queryset =  receive_note.objects.all()
    serializer_class = receive_note_Serializer
    permission_classes = [IsAuthenticated]           
    
    def _check_complete_transfer(self, transfer_note_obj):
        """Check if all items in transfer note have been fully received"""
        transfer_details = transfer_note_detail.objects.filter(transfer_note=transfer_note_obj)
        receive_notes = receive_note.objects.filter(transfer_note=transfer_note_obj)
        
        all_received = True
        for transfer_detail in transfer_details:
            total_received = receive_note_detail.objects.filter(
                receive_note__in=receive_notes,
                item=transfer_detail.item
            ).aggregate(total=Sum('quantity'))['total'] or 0
            
            if total_received < transfer_detail.quantity:
                all_received = False
                break
        
        if all_received:
            transfer_note_obj.status = 'delivered'
            transfer_note_obj.save()    
        

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            current_user = request.user
            if not hasattr(current_user, 'store') or not current_user.store:
                raise ValidationError("User is not associated with any store")
            
            store = current_user.store
            transfer_note_id = request.data.get('transfer_note_id')
            items_data = request.data.get('items', [])
            
            if not transfer_note_id:
                raise ValidationError("Transfer note ID is required")
            
            try:
                transfer_note_obj = transfer_note.objects.select_related('warehouse').get(id=transfer_note_id)
            except transfer_note.DoesNotExist:
                raise ValidationError(f"Transfer note {transfer_note_id} not found")
            
            # Verify the transfer note is for this store
            if transfer_note_obj.request_note and transfer_note_obj.request_note.store != store:
                raise ValidationError("This transfer note is not intended for your store")
            
            # Create the receive note
            receive_note_obj = receive_note.objects.create(
                transfer_note=transfer_note_obj,
                store=store,
                received_by=current_user,
                warehouse=transfer_note_obj.warehouse,
                status='received'
            )
            
            # Process each item
            for item_data in items_data:
                item_id = item_data.get('item_id')
                quantity = int(item_data.get('quantity', 0))
                
                if quantity <= 0:
                    raise ValidationError(f"Quantity must be positive for item {item_id}")
                
                try:
                    # Verify the item exists in the transfer note
                    transfer_detail = transfer_note_detail.objects.get(
                        transfer_note=transfer_note_obj,
                        item_id=item_id
                    )
                    
                    # Validate quantity doesn't exceed transferred quantity
                    if quantity > transfer_detail.quantity:
                        raise ValidationError(
                            f"Cannot receive more than transferred quantity for item {item_id} "
                            f"(Transferred: {transfer_detail.quantity}, Received: {quantity})"
                        )
                    
                    # Create receive note detail
                    receive_note_detail.objects.create(
                        item_id=item_id,
                        receive_note=receive_note_obj,
                        quantity=quantity
                    )
                    
                    # Update stockitems
                    item = items.objects.get(id=item_id)
                    stock, created = stock_items.objects.get_or_create(
                        store=store,
                        item=item,
                        defaults={'quantity': quantity}
                    )
                    
                    if not created:
                        stock.quantity = F('quantity') + quantity
                        stock.save()
                        stock.refresh_from_db()
                    
                except transfer_note_detail.DoesNotExist:
                    raise ValidationError(f"Item {item_id} not found in transfer note {transfer_note_id}")
                except items.DoesNotExist:
                    raise ValidationError(f"Item {item_id} not found")
            
            # Update transfer note status if all items are received
            self._check_complete_transfer(transfer_note_obj)
            
            return Response({
                'message': 'Receive note created successfully',
                'receive_note_id': receive_note_obj.id,
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class receive_note_detail_ViewSet( CustomCreateMixin, CustomUpdateMixin, CustomDestroyMixin, viewsets.ModelViewSet):
    queryset = receive_note_detail.objects.all()
    serializer_class = receive_note_detail_Serializer
    permission_classes = [IsAuthenticated]

class warehouse_stock_ViewSet(CustomCreateMixin,CustomUpdateMixin, CustomDestroyMixin, viewsets.ModelViewSet):
    queryset = warehouse_stock.objects.all()
    serializer_class = warehouse_stock_Serializer
    permission_classes = [IsAuthenticated]

class inventory_adjustments_ViewSet(CustomUpdateMixin, CustomCreateMixin, CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = inventory_adjustments.objects.all()
    serializer_class = inventory_adjustments_Serializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                item = data['item']
                quantity = data['quantity']
                adjustment_type = data['adjustment_type']
                reason = data.get('adjustment_reason', '')
                adjusted_by = data['adjusted_by']  

                # Validate adjustment type
                if adjustment_type not in ['Damage', 'Unsold_items']:
                    return Response(
                        {'error': 'Only Damage or Unsold_items adjustments are allowed'},
                        status=400
                    )   

                # Check stock
                stock = stock_items.objects.get(item=item)
                if stock.quantity < quantity:
                    return Response(
                        {'error': f'Only {stock.quantity} items in stock. Cannot adjust {quantity}.'},
                        status=400
                    )

                # Create inventory adjustment
                inventory_adjustments.objects.create(
                    item=item,
                    quantity=quantity,
                    adjustment_type=adjustment_type,
                    adjustment_reason=reason,
                    adjusted_by=adjusted_by,
                    sales_order_return=None,
                    created_at=timezone.now(),
                    is_processed=False
                )

                # Update stock
                stock.quantity -= quantity
                stock.save()
                check_safety_stock(item)

                return Response({
                    'status': "success",
                    'message': f'{quantity} units of {item.item_name} removed from stock',
                    'remaining_stock': stock.quantity
                }, status=201)

            except stock_items.DoesNotExist:
                return Response({'error': 'Item not in stock'}, status=400)
            except Exception as e:
                return Response({'error': str(e)}, status=400)

        return Response(serializer.errors, status=400)

    
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
    

class purchase_order_return_ViewSet(viewsets.ModelViewSet):
    queryset = purchase_order_return.objects.all()
    serializer_class = purchase_order_return_Serializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request):
        serializer = purchase_order_return_Serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                adjustment_ids = data.get('adjustment_ids')
                created_by = request.user

                valid_adjustments = inventory_adjustments.objects.filter(
                    id__in=adjustment_ids,
                    adjustment_type__in=['Unsold_items', 'Damage'],
                    is_processed=False
                )
                
                if valid_adjustments.count() != len(adjustment_ids):
                    invalid_ids = set(adjustment_ids) - set(valid_adjustments.values_list('id', flat=True))
                    return Response(
                        {'error': f'Invalid or already processed adjustments: {invalid_ids}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                total_refund = Decimal('0')
                return_items = []
                vendor = None

                for adj in valid_adjustments:
                    try:
                        po_detail = purchase_order_detail.objects.filter(
                            item=adj.item
                        ).order_by('-purchase_order__created_at').first()
                        
                        if not po_detail:
                            raise Exception(f"No purchase found for item {adj.item.id}")

                        if not vendor:
                            vendor = po_detail.purchase_order.vendor
                        elif vendor != po_detail.purchase_order.vendor:
                            return Response(
                                {'error': 'All items must belong to same vendor'},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        refund_amount = po_detail.price_per_piece * adj.quantity
                        total_refund += refund_amount
                        return_items.append({
                            'item': adj.item,
                            'quantity': adj.quantity,
                            'price': po_detail.price_per_piece,
                            'refund': refund_amount,
                            'purchase_order': po_detail.purchase_order,
                            'adjustment': adj
                        })

                    except Exception as e:
                        return Response(
                            {'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                if not return_items:
                    return Response(
                        {'error': 'No valid items found for processing'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Create return header
                return_header = purchase_order_return.objects.create(
                    purchase_orders=return_items[0]['purchase_order'],
                    vendor=vendor,
                    total_refund_amount=total_refund,
                    created_at=timezone.now(),
                    created_by=created_by
                )

                for item in return_items:
                    # Create return detail
                    purchase_order_return_detail.objects.create(
                        return_purchase=return_header,
                        purchase_order_detail=purchase_order_detail.objects.get(
                            item=item['item'],
                            purchase_order=item['purchase_order']
                        ),
                        return_quantity=item['quantity'],
                        price_per_piece=item['price'],
                        subtotal=item['refund'],
                        created_at=timezone.now()
                    )

                    # Mark adjustment as processed
                    item['adjustment'].is_processed = True
                    item['adjustment'].save()

                # Process vendor refund using correct field
                self._process_vendor_refund(vendor, total_refund)

                return Response({
                    'message': 'Purchase return processed successfully',
                    'return_id': return_header.id,
                    'total_refund': str(total_refund),
                    'vendor_id': vendor.id,
                    'vendor_name': vendor.vendor_name  
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _process_vendor_refund(self, vendor, amount):
        """Handle vendor refund processing using correct field"""
        vendor.total_payables = (vendor.total_payables or Decimal('0')) - amount
        vendor.save()        


    
class purchase_order_return_detail_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = purchase_order_return_detail.objects.all()
    serializer_class = purchase_order_return_detail_Serializer
    permission_classes = [IsAuthenticated]



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
        
class tax_configurations_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = tax_configurations.objects.all()
    serializer_class = tax_configurations_Serializer
    permission_classes = [IsAuthenticated]
    
class AuthUser_ViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Custom_User.objects.all()
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


def get_daily_sales(date=None):
    """Calculate daily sales for a specific date (defaults to today)"""
    if date is None:
        date = timezone.now().date()
    
    start_date = timezone.make_aware(datetime.combine(date, datetime.min.time()))
    end_date = timezone.make_aware(datetime.combine(date, datetime.max.time()))
    
    return sales_orders.objects.filter(
        created_at__range=(start_date, end_date)
    ).aggregate(
        total_sales=Sum('net_total'),
        total_orders=Count('id')
    )


def get_monthly_sales(year=None, month=None):
    """Calculate monthly sales for a specific year/month (defaults to current)"""
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().month
    
    print(f"Fetching monthly sales for {year}-{month}")
    
    # Get first and last day of month for precise filtering
    first_day = timezone.make_aware(datetime(year, month, 1))
    if month == 12:
        last_day = timezone.make_aware(datetime(year+1, 1, 1) - timedelta(days=1))
    else:
        last_day = timezone.make_aware(datetime(year, month+1, 1) - timedelta(days=1))
    
    result = sales_orders.objects.filter(
        created_at__range=(first_day, last_day)
    ).aggregate(
        total_sales=Sum('net_total'),
        total_orders=Count('id')
    )
    
    print(f"Monthly sales result: {result}")
    
    return result

def get_yearly_sales(year=None):
    """Calculate yearly sales for a specific year (defaults to current)"""
    if year is None:
        year = timezone.now().year
    
    return sales_orders.objects.filter(
        created_at__year=year
    ).aggregate(
        total_sales=Sum('net_total'),
        total_orders=Count('id')
    )

class SalesReportAPIView(APIView):
    """
    POST API View to get sales summary for daily, monthly, or yearly reports.
    Default = today's report if no report_type is specified.
    """
    def post(self, request):
        report_type = request.data.get('report_type', 'daily')
        custom_date = request.data.get('custom_date')         # YYYY-MM-DD
        custom_month = request.data.get('custom_month')       # YYYY-MM
        custom_year = request.data.get('custom_year')         # YYYY

        sales_data = {}
        period_label = ""

        try:
            if report_type == 'daily':
                if custom_date:
                    date = datetime.strptime(custom_date, '%Y-%m-%d').date()
                    sales_data = get_daily_sales(date)
                    period_label = date.strftime("%d %b %Y")
                else:
                    sales_data = get_daily_sales()
                    period_label = "Today"

            elif report_type == 'monthly':
                if custom_month:
                    year, month = map(int, custom_month.split('-'))
                    sales_data = get_monthly_sales(year, month)
                    period_label = datetime(year, month, 1).strftime("%B %Y")
                else:
                    sales_data = get_monthly_sales()
                    period_label = "This Month"

            elif report_type == 'yearly':
                if custom_year:
                    year = int(custom_year)
                    sales_data = get_yearly_sales(year)
                    period_label = str(year)
                else:
                    sales_data = get_yearly_sales()
                    period_label = "This Year"

            else:
                return Response({"error": "Invalid report_type. Use 'daily', 'monthly', or 'yearly'."},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "report_type": report_type,
            "period": period_label,
            "total_sales": sales_data.get("total_sales", 0) or 0,
            "total_orders": sales_data.get("total_orders", 0) or 0
        }, status=status.HTTP_200_OK)


def get_daily_purchases(date=None):
    """Calculate daily purchases for a specific date (defaults to today)"""
    if date is None:
        date = timezone.now().date()
    
    start_date = timezone.make_aware(datetime.combine(date, datetime.min.time()))
    end_date = timezone.make_aware(datetime.combine(date, datetime.max.time()))
    
    return purchase_orders.objects.filter(
        created_at__range=(start_date, end_date)
    ).aggregate(
        total_purchases=Sum('net_total'),
        total_orders=Count('id')
    )

def get_monthly_purchases(year=None, month=None):
    """Calculate monthly purchases for a specific year/month (defaults to current)"""
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().month
    
    # Get first and last day of month for precise filtering
    first_day = timezone.make_aware(datetime(year, month, 1))
    if month == 12:
        last_day = timezone.make_aware(datetime(year+1, 1, 1) - timedelta(days=1))
    else:
        last_day = timezone.make_aware(datetime(year, month+1, 1) - timedelta(days=1))
    
    return purchase_orders.objects.filter(
        created_at__range=(first_day, last_day)
    ).aggregate(
        total_purchases=Sum('net_total'),
        total_orders=Count('id')
    )

def get_yearly_purchases(year=None):
    """Calculate yearly purchases for a specific year (defaults to current)"""
    if year is None:
        year = timezone.now().year
    
    return purchase_orders.objects.filter(
        created_at__year=year
    ).aggregate(
        total_purchases=Sum('net_total'),
        total_orders=Count('id')
    )

class PurchaseReportAPIView(APIView):    
    def post(self, request):
        report_type = request.data.get('report_type', 'daily')
        custom_date = request.data.get('custom_date')         # YYYY-MM-DD
        custom_month = request.data.get('custom_month')       # YYYY-MM
        custom_year = request.data.get('custom_year')         # YYYY

        purchase_data = {}
        period_label = ""

        try:
            if report_type == 'daily':
                if custom_date:
                    date = datetime.strptime(custom_date, '%Y-%m-%d').date()
                    purchase_data = get_daily_purchases(date)
                    period_label = date.strftime("%d %b %Y")
                else:
                    purchase_data = get_daily_purchases()
                    period_label = "Today"

            elif report_type == 'monthly':
                if custom_month:
                    year, month = map(int, custom_month.split('-'))
                    purchase_data = get_monthly_purchases(year, month)
                    period_label = datetime(year, month, 1).strftime("%B %Y")
                else:
                    purchase_data = get_monthly_purchases()
                    period_label = "This Month"

            elif report_type == 'yearly':
                if custom_year:
                    year = int(custom_year)
                    purchase_data = get_yearly_purchases(year)
                    period_label = str(year)
                else:
                    purchase_data = get_yearly_purchases()
                    period_label = "This Year"

            else:
                return Response({"error": "Invalid report_type. Use 'daily', 'monthly', or 'yearly'."},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "report_type": report_type,
            "period": period_label,
            "total_purchases": purchase_data.get("total_purchases", 0) or 0,
            "total_orders": purchase_data.get("total_orders", 0) or 0,
            # "average_order_value": (purchase_data.get("total_purchases", 0) or 0) / 
            #                      (purchase_data.get("total_orders", 1) or 1)
        }, status=status.HTTP_200_OK)

