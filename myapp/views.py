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



from rest_framework import viewsets,mixins
from .models import Categories,SalesOrderDetail, Area, Customers, Discounts, Inventoryadjustments, Items, Purchaseorders, Purchasereceipts, User, SalesorderDiscounts, Salesorders, Salesordertax, Shipments, StockItems, Stockmanagement, Taxconfigurations,  Vendors, Warehouses
from .serializers import CategoriesSerializer,SalesOrderDetailSerializer, PlaceOrderSerializer,AreaSerializer, CustomersSerializer, DiscountsSerializer, InventoryadjustmentsSerializer, ItemsSerializer, PurchaseordersSerializer, PurchasereceiptsSerializer, SalesorderDiscountsSerializer, SalesordersSerializer, SalesordertaxSerializer, ShipmentsSerializer, StockItemsSerializer, StockmanagementSerializer, TaxconfigurationsSerializer, AuthUserSerializer, VendorsSerializer, WarehousesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomTokenRefreshSerializer
from django.db import models
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.core.exceptions import ValidationError
import time
from django.utils import timezone

class PlaceOrderViewSet(viewsets.ViewSet):
    @transaction.atomic
    def create(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                customer_id = data.get('customer_id')
                area_id = data.get('area_id')
                order_details = data.get('order_details')

                # Validate customer
                customer = Customers.objects.get(id=customer_id)

                # Validate area
                area = Area.objects.get(id=area_id)

                # Initialize order totals
                total_amount = 0
                total_discount = 0
                total_tax = 0
                net_total = 0

                # Create sales order
                sales_order = Salesorders(
                    sales_order_number=f"SO{customer_id}{int(time.time())}",  # Generate unique order number
                    customer=customer,
                    area=area,
                    order_status='Pending',
                    total_amount=0,  # Will be updated later
                    discount=0,  # Will be updated later
                    tax_amount=0,  # Will be updated later
                    net_total=0,  # Will be updated later
                    created_at=timezone.now()
                )
                sales_order.save()

                # Process each item in the order
                for item_detail in order_details:
                    item_id = item_detail.get('item_id')
                    quantity = int(item_detail.get('quantity'))  # Convert quantity to integer
                    discount_id = item_detail.get('discount_id')

                    # Validate item
                    item = Items.objects.get(id=item_id)

                    # Retrieve the related StockItems instance
                    stock_item = item.stock_items.first()  # Use .first() to get a single instance
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
                        discount = Discounts.objects.get(id=discount_id)
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
                    sales_order_detail = SalesOrderDetail(
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
                    sales_order_detail.save()

                    # Update stock
                    stock_item.quantity = stock_quantity - quantity
                    stock_item.save()

                # Add delivery charges to the total
                net_total += area.delivery_charges

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
        # Get username and password from request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            # Generate JWT tokens
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
            # Invalid credentials
            return Response({
                'message': 'Invalid credentials',
            }, status=status.HTTP_401_UNAUTHORIZED)

class CustomCreateMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        # Save the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Return custom response
        return Response({
            "status": "success",
            "message": "Data created successfully"
        }, status=status.HTTP_201_CREATED)

class CustomDestroyMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        # Delete the data
        instance = self.get_object()
        self.perform_destroy(instance)

        # Return custom response
        return Response({
            "status": "success",
            "message": "Data deleted successfully"
        }, status=status.HTTP_200_OK)


class CustomUpdateMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        # Get instance
        instance = self.get_object()
        
        # Check for extra fields
        model_fields = [f.name for f in instance._meta.get_fields()]  # Get all model fields
        extra_fields = set(request.data.keys()) - set(model_fields)  # Find extra fields
        
        if extra_fields:
            return Response({
                "status": "error",
                "message": f"Invalid fields: {', '.join(extra_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate and update data
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
        total_sales = Salesorders.objects.aggregate(total_sales=models.Sum('total_amount'))
        return Response({'total_sales': total_sales['total_sales']})

class PurchaseReportView(APIView):
    def get(self, request):
        total_purchases = Purchaseorders.objects.aggregate(total_purchases=models.Sum('total_amount'))
        return Response({'total_purchases': total_purchases['total_purchases']})

class CategoriesViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]

class CustomersViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    permission_classes = [IsAuthenticated]

class DiscountsViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Discounts.objects.all()
    serializer_class = DiscountsSerializer
    permission_classes = [IsAuthenticated]

class InventoryadjustmentsViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Inventoryadjustments.objects.all()
    serializer_class = InventoryadjustmentsSerializer
    permission_classes = [IsAuthenticated]

class ItemsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]


class PurchaseordersViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Purchaseorders.objects.all()
    serializer_class = PurchaseordersSerializer
    permission_classes = [IsAuthenticated]

class PurchasereceiptsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Purchasereceipts.objects.all()
    serializer_class = PurchasereceiptsSerializer
    permission_classes = [IsAuthenticated]

class SalesorderDiscountsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = SalesorderDiscounts.objects.all()
    serializer_class = SalesorderDiscountsSerializer
    permission_classes = [IsAuthenticated]

class SalesordersViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Salesorders.objects.all()
    serializer_class = SalesordersSerializer
    permission_classes = [IsAuthenticated]
    
class SalesordertaxViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Salesordertax.objects.all()
    serializer_class = SalesordertaxSerializer
    permission_classes = [IsAuthenticated]
    
class ShipmentsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentsSerializer
    permission_classes = [IsAuthenticated]
    
class StockItemsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = StockItems.objects.all()
    serializer_class = StockItemsSerializer
    permission_classes = [IsAuthenticated]
    
class StockmanagementViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Stockmanagement.objects.all()
    serializer_class = StockmanagementSerializer
    permission_classes = [IsAuthenticated]
    
class TaxconfigurationsViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Taxconfigurations.objects.all()
    serializer_class = TaxconfigurationsSerializer
    permission_classes = [IsAuthenticated]
    
class AuthUserViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = [IsAuthenticated]
    
class VendorsViewSet(CustomCreateMixin,CustomUpdateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Vendors.objects.all()
    serializer_class = VendorsSerializer
    permission_classes = [IsAuthenticated]
    
class WarehousesViewSet(CustomCreateMixin,CustomDestroyMixin,CustomUpdateMixin,viewsets.ModelViewSet):
    queryset = Warehouses.objects.all()
    serializer_class = WarehousesSerializer
    permission_classes = [IsAuthenticated]
    
    
class AreaViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]
    
class SalesOrderDetailViewSet(CustomUpdateMixin,CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = SalesOrderDetail.objects.all()
    serializer_class = SalesOrderDetailSerializer
    permission_classes = [IsAuthenticated]