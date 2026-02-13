from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.mail import send_mail

from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'], url_path='set-status')
    def set_status(self,requst,pk=None):
        order=self.get_object()
        new_status = requst.data.get('status')

        if new_status not in dict (Order.STATUS_CHOICES).keys():
            return Response({'error':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        old_status = order.status
        order.status = new_status
        order.save()

        if old_status != new_status:
            send_mail(
                subject=f'Update order status: {order.product_name}',
                message=f'Hello, dear {order.customer_name}!\nYour order change status to: {order.get_status_display()}',
                from_email='shop@example.com',
                recipient_list=[order.customer_email],
                fail_silently=False
            )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
