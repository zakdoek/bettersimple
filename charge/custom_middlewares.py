from django.conf import settings

import stripe

class StripeMiddleware(object):
    def process_request(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
