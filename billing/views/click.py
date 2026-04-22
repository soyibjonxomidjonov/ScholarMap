from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from billing.models import Transaction
from billing.serializer import TransactionSerializer
from billing.utils import check_click_sign
from api.models import User




class ClickPaymentView(APIView):
    def post(self, request):
        data = request.data

        sign = check_click_sign(data, settings.CLICK_SECRET_KEY)

        if sign != data.get('sign_string'):
            return Response({"error": -1, "error_note": "Invalid sign"})

        try:
            user = User.objects.get(id=data.get('merchant_trans_id'))
        except User.DoesNotExist:
            return Response({"error": -5, "error_note": "User not found"})

        Transaction.objects.get_or_create(
            transaction_id=data.get('click_trans_id'),
            defaults={
                'user': user,
                'amount': data.get('amount'),
                'provider': 'click',
                'status': 'pending',
            }
        )

        return Response({
            "click_trans_id": data.get('click_trans_id'),
            "merchant_trans_id": data.get('merchant_trans_id'),
            "merchant_prepare_id": user.id,
            "error": 0,
            "error_note": "Success"
        })


class ClickCompleteView(APIView):
    def post(self, request):

        data = request.data

        sign = check_click_sign(data, settings.CLICK_SECRET_KEY)
        if sign != data.get('sign_string'):
            return Response({"error": -1, "error_note": "Invalid sign"})

        try:
            transaction = Transaction.objects.get(transaction_id=data.get('click_trans_id'))

        except Transaction.DoesNotExist:
            return Response({"error": -6, "error_note": "Transaction not found"})

        if int(data.get('error', 0)) < 0:
            transaction.status = 'cancelled'
            transaction.save()
            return Response({"error": 0, "error_note": "Cancelled"})

        transaction.status = 'completed'
        transaction.save()

        user = transaction.user
        user.tarif = 'premium'
        user.save()
        return Response({
            "click_trans_id": data.get('click_trans_id'),
            "merchant_trans_id": data.get('merchant_trans_id'),
            "merchant_confirm_id": user.id,
            "error": 0,
            "error_note": "Success"
        })


class ClickCreatePaymentView(APIView):
    def post(self, request):

        serializer = TransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        amount = serializer.validated_data['amount']
        user = request.user

        payment_url = (
            f"https://my.click.uz/services/pay"
            f"?service_id={settings.CLICK_SERVICE_ID}"
            f"&merchant_id={settings.CLICK_MERCHANT_ID}"
            f"&amount={amount}"
            f"&transaction_param={user.id}"        )


        return Response({
            "payment_url": payment_url
        })
