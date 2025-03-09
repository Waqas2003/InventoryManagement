from rest_framework import viewsets
from .models import Categories, Customers, Discounts, Inventoryadjustments, Items, Pricelists, Purchaseorders, Purchasereceipts, SalesorderDiscounts, Salesorders, Salesordertax, Shipments, StockItems, Stockmanagement, Taxconfigurations, Users, Vendors, Warehouses
from .serializers import CategoriesSerializer, CustomersSerializer, DiscountsSerializer, InventoryadjustmentsSerializer, ItemsSerializer, PricelistsSerializer, PurchaseordersSerializer, PurchasereceiptsSerializer, SalesorderDiscountsSerializer, SalesordersSerializer, SalesordertaxSerializer, ShipmentsSerializer, StockItemsSerializer, StockmanagementSerializer, TaxconfigurationsSerializer, UsersSerializer, VendorsSerializer, WarehousesSerializer

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer

class DiscountsViewSet(viewsets.ModelViewSet):
    queryset = Discounts.objects.all()
    serializer_class = DiscountsSerializer

class InventoryadjustmentsViewSet(viewsets.ModelViewSet):
    queryset = Inventoryadjustments.objects.all()
    serializer_class = InventoryadjustmentsSerializer

class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer

class PricelistsViewSet(viewsets.ModelViewSet):
    queryset = Pricelists.objects.all()
    serializer_class = PricelistsSerializer

class PurchaseordersViewSet(viewsets.ModelViewSet):
    queryset = Purchaseorders.objects.all()
    serializer_class = PurchaseordersSerializer

class PurchasereceiptsViewSet(viewsets.ModelViewSet):
    queryset = Purchasereceipts.objects.all()
    serializer_class = PurchasereceiptsSerializer

class SalesorderDiscountsViewSet(viewsets.ModelViewSet):
    queryset = SalesorderDiscounts.objects.all()
    serializer_class = SalesorderDiscountsSerializer

class SalesordersViewSet(viewsets.ModelViewSet):
    queryset = Salesorders.objects.all()
    serializer_class = SalesordersSerializer

class SalesordertaxViewSet(viewsets.ModelViewSet):
    queryset = Salesordertax.objects.all()
    serializer_class = SalesordertaxSerializer

class ShipmentsViewSet(viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentsSerializer

class StockItemsViewSet(viewsets.ModelViewSet):
    queryset = StockItems.objects.all()
    serializer_class = StockItemsSerializer

class StockmanagementViewSet(viewsets.ModelViewSet):
    queryset = Stockmanagement.objects.all()
    serializer_class = StockmanagementSerializer

class TaxconfigurationsViewSet(viewsets.ModelViewSet):
    queryset = Taxconfigurations.objects.all()
    serializer_class = TaxconfigurationsSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class VendorsViewSet(viewsets.ModelViewSet):
    queryset = Vendors.objects.all()
    serializer_class = VendorsSerializer

class WarehousesViewSet(viewsets.ModelViewSet):
    queryset = Warehouses.objects.all()
    serializer_class = WarehousesSerializer