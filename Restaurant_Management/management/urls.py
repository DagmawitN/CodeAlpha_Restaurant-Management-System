from rest_framework.routers import DefaultRouter
from .views import (MenuItemViewSet,TableViewSet,ReservationViewSet,OrderViewSet,InventoryViewSet)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet)
router.register(r'tables', TableViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = router.urls