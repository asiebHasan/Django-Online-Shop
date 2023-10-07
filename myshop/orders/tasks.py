# tasks.py
from celery import Celery
from django.core.mail import send_mail
from .models import Order

app = Celery()


@app.task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order no. {order.id}'
    # Build the message with order details
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order. Your order ID is {order.id}.\n\n' \
              f'Order Details:\n'
    
     # Add information about each ordered item
    for item in order.items.all():
        message += f'- Product: {item.product}\n' \
                   f'  Quantity: {item.quantity}\n' \
                   f'  Price per item: ${item.price:.2f}\n' \
                   f'  Subtotal: ${item.get_cost():.2f}\n\n'
    
    # Add the total price of the order
    message += f'Total Price: ${order.get_total_cost():.2f}\n\n'

    
    mail_sent = send_mail(subject,
                          message,
                          'asieb.hasan.supto@gmail.com',
                          [order.email])
    return mail_sent
