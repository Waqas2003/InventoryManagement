from rest_framework import viewsets,mixins
from .models import Categories, Customers, Discounts, Inventoryadjustments, Items, Pricelists, Purchaseorders, Purchasereceipts, AuthUser, SalesorderDiscounts, Salesorders, Salesordertax, Shipments, StockItems, Stockmanagement, Taxconfigurations,  Vendors, Warehouses
from .serializers import CategoriesSerializer, CustomersSerializer, DiscountsSerializer, InventoryadjustmentsSerializer, ItemsSerializer, PricelistsSerializer, PurchaseordersSerializer, PurchasereceiptsSerializer, SalesorderDiscountsSerializer, SalesordersSerializer, SalesordertaxSerializer, ShipmentsSerializer, StockItemsSerializer, StockmanagementSerializer, TaxconfigurationsSerializer, AuthUserSerializer, VendorsSerializer, WarehousesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

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

class CategoriesViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]

class CustomersViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    permission_classes = [IsAuthenticated]

class DiscountsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Discounts.objects.all()
    serializer_class = DiscountsSerializer
    permission_classes = [IsAuthenticated]

class InventoryadjustmentsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Inventoryadjustments.objects.all()
    serializer_class = InventoryadjustmentsSerializer
    permission_classes = [IsAuthenticated]

class ItemsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]

class PricelistsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Pricelists.objects.all()
    serializer_class = PricelistsSerializer
    permission_classes = [IsAuthenticated]

class PurchaseordersViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Purchaseorders.objects.all()
    serializer_class = PurchaseordersSerializer
    permission_classes = [IsAuthenticated]

class PurchasereceiptsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Purchasereceipts.objects.all()
    serializer_class = PurchasereceiptsSerializer
    permission_classes = [IsAuthenticated]

class SalesorderDiscountsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = SalesorderDiscounts.objects.all()
    serializer_class = SalesorderDiscountsSerializer
    permission_classes = [IsAuthenticated]

class SalesordersViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Salesorders.objects.all()
    serializer_class = SalesordersSerializer
    permission_classes = [IsAuthenticated]
    
class SalesordertaxViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Salesordertax.objects.all()
    serializer_class = SalesordertaxSerializer
    permission_classes = [IsAuthenticated]
    
class ShipmentsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentsSerializer
    permission_classes = [IsAuthenticated]
    
class StockItemsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = StockItems.objects.all()
    serializer_class = StockItemsSerializer
    permission_classes = [IsAuthenticated]
    
class StockmanagementViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Stockmanagement.objects.all()
    serializer_class = StockmanagementSerializer
    permission_classes = [IsAuthenticated]
    
class TaxconfigurationsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Taxconfigurations.objects.all()
    serializer_class = TaxconfigurationsSerializer
    permission_classes = [IsAuthenticated]
    
class AuthUserViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = [IsAuthenticated]
    
class VendorsViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Vendors.objects.all()
    serializer_class = VendorsSerializer
    permission_classes = [IsAuthenticated]
    
class WarehousesViewSet(CustomCreateMixin,CustomDestroyMixin,viewsets.ModelViewSet):
    queryset = Warehouses.objects.all()
    serializer_class = WarehousesSerializer
    permission_classes = [IsAuthenticated]