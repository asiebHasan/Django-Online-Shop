from io import BytesIO
from celery import Celery
import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from orders.models import Order

app = Celery()


@app.task
def payment_completed(order_id):
    """
    Task to send an email notification when order in successfully created
    """

    order = Order.objects.get(id=order_id)

    # create invoice email
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'

    email = EmailMessage(subject,
                         message,
                         'asieb.hasan.supto@gmail.com',
                         [order.email])

    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach PDF file
    email.attach(f'Order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # send e-mail
    email.send()
