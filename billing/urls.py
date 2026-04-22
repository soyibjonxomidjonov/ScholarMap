from django.urls import path
from billing.views import ClickPaymentView, ClickCompleteView, ClickCreatePaymentView

urlpatterns = [
    path('click/', ClickPaymentView.as_view(), name='click-payment'),
    path('click/complete/', ClickCompleteView.as_view(), name='click-complete'),
    path('click/pay/', ClickCreatePaymentView.as_view(), name='click-pay'),
]