from django.conf import settings
from iamport import Iamport
from django.utils.functional import cached_property
from django.utils import timezone
import logging
import json

# logger = logging.getLogger('apps.payments')

@cached_property
def api(self):
    return Iamport(
        imp_key=settings.PORTONE_API_KEY, imp_secret=settings.PORTONE_API_SECRET
    )

def get_portone_token():
    iamport = Iamport(imp_key=settings.PORTONE_API_KEY, imp_secret=settings.PORTONE_API_SECRET)
    response = iamport._get_token()
    if response['code'] != 0:
        raise Exception('Failed to get Portone token: {}'.format(response['message']))
    return response['response']['access_token']


def schedule_payment(customer_uid, merchant_uid, amount, schedule_at, name):
    iamport = Iamport(imp_key=settings.PORTONE_API_KEY, imp_secret=settings.PORTONE_API_SECRET)
    
    payload = {
        "customer_uid" : customer_uid,
        "schedules" : [
            {
                "merchant_uid" : merchant_uid,
                "amount" : float(amount),
                "schedule_at" : schedule_at, 
                "name" : name
            }
        ]
    }

    response = iamport.pay_schedule(**payload)
    
    return response

def cancel_scheduled_payment(customer_uid, merchant_uid):
    iamport = Iamport(imp_key=settings.PORTONE_API_KEY, imp_secret=settings.PORTONE_API_SECRET)

    payload = {
        "customer_uid" : customer_uid,
        "merchant_uid" : merchant_uid,
    }

    response = iamport.pay_unschedule(**payload)
    
    return response