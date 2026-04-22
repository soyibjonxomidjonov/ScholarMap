from django.urls import path
from billing.views import ClickPaymentView, ClickCompleteView, ClickCreatePaymentView

urlpatterns = [
    path('click/pay/', ClickCreatePaymentView.as_view(), name='click-pay'),          # havola yaratish
    path('click/prepare/', ClickPaymentView.as_view(), name='click-prepare'),        # Click webhook 1
    path('click/complete/', ClickCompleteView.as_view(), name='click-complete'),
]