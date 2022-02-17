from django.http import HttpResponse
from django.shortcuts import redirect , get_object_or_404 , render
import requests
import json
from orders.models import Order
from courses.models import Course
from cart.cart import Cart

MERCHANT = '1344b5d4-0048-11e8-94db-005056a205be'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:3000/zarinpal/verify/'


def send_request(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order , id=order_id)
    total_cost = order.get_total_cost()
    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_cost,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": order.email }
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order , id=order_id)
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_cost(),
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                # return HttpResponse('Transaction success.\nRefID: ' + str(
                #     req.json()['data']['ref_id']
                # ))
                order.paid = True
                order.save()
                for item in order.items.all():
                    item.course.student.add(request.user)

                return render(request , 'zarinpal/success.html')
            elif t_status == 101:
                # return HttpResponse('Transaction submitted : ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request,'zarinpal/submited.html' ,{'status':str(
                    req.json()['data']['message']
                )})
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request,'zarinpal/failed.html' , {'status': str(
                    req.json()['data']['message']
                )})
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request , 'zarinpal/failed.html' , {'e_code':e_code,'e_message':e_message})
    else:
        # return HttpResponse('Transaction failed or canceled by user')
        return render(request,'zarinpal/cancel.html')