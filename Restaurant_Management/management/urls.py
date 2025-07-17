from rest_framework.routers import DefaultRouter
from .views import (MenuItemViewSet,AvailableMenuItemViewSet,TableViewSet,AvailableTableViewSet,ReservationViewSet,OrderViewSet,InventoryViewSet)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet)
router.register(r'available-menu-items', AvailableMenuItemViewSet, basename='available-menu-items')
router.register(r'tables', TableViewSet)
router.register(r'available-tables', AvailableTableViewSet, basename='available-tables')
router.register(r'reservations', ReservationViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = router.urls