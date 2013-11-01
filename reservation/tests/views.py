from datetime import datetime, timedelta
from django.utils import unittest
from django.test import client

from reservation.models import *
from common.test_helpers import *
from reservation import types

# Create user
# Create company
# Hook user to company via profile
# Create reservations
    

class IndextTestCase(unittest.TestCase):
    """ Tests the index method of the view."""
    def setUp(self):
        (self.username, self.password, self.user, self.company) = create_company()
        self.test_client = client.Client()
        self.test_client.login(username=self.username, password=self.password)
    
    def setUp_for_trips(self):
        (self.username, self.password, self.user, self.company) = create_company(reservation_type=types.TRIP)
        self.test_client = client.Client()
        self.test_client.login(username=self.username, password=self.password)
    
    def tearDown(self):
        if self.company.industry_profile.reservation_type == types.APPOINTMENT:
            for reservation in Reservation.objects.filter(company=self.company):
                reservation.delete()
                reservation.customer.delete()
        else:
            for trip in Trip.objects.filter(company=self.company):
                trip.delete()
                trip.customer.delete()
                trip.pickup_address.delete()
                trip.dropoff_address.delete()
            
        self.user.profile.delete()
        self.company.delete()
        self.user.delete()
        
    def test_page_is_not_integer(self):
        self.reservations = create_reservations(self.company, create_past_reservations=False, amount=5)
        response = self.test_client.get('/reservation/?page=test', **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.context['reservations'].number, 1)
        self.assertEqual(response.context['has_reservations'], True)
        self.assertEqual(len(response.context['reservations']), len(self.reservations))
        self.assertEqual(response.context['client'], self.company)
        self.assertEqual(response.context['search_terms'], "")
        self.assertEqual(response.context['start_date'], "")
        self.assertEqual(response.context['end_date'], "")
        self.assertEqual(response.context['show_past'], False)
        self.assertEqual(response.context['show_confirmation'], None)
        self.assertEqual(response.context['confirmation_message'], None)
        self.assertEqual(response.context['has_past_reservations'], False)
    
    def test_page_is_not_integer_trips(self):
        self.tearDown()
        self.setUp_for_trips()
        self.test_page_is_not_integer()
    
    def test_page_integer_exceeds_size(self):
        self.reservations = create_reservations(self.company, create_past_reservations=False, amount=5)
        response = self.test_client.get('/reservation/?page=100', **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.context['reservations'].number, 1)
        self.assertEqual(response.context['has_reservations'], True)
        self.assertEqual(len(response.context['reservations']), len(self.reservations))
        self.assertEqual(response.context['client'], self.company)
        self.assertEqual(response.context['search_terms'], "")
        self.assertEqual(response.context['start_date'], "")
        self.assertEqual(response.context['end_date'], "")
        self.assertEqual(response.context['show_past'], False)
        self.assertEqual(response.context['show_confirmation'], None)
        self.assertEqual(response.context['confirmation_message'], None)
        self.assertEqual(response.context['has_past_reservations'], False)
    
    def test_page_integer_exceeds_size_trips(self):
        self.tearDown()
        self.setUp_for_trips()
        self.test_page_integer_exceeds_size()
    
    def test_search_variables_not_valid(self):
        self.reservations = create_reservations(self.company, create_past_reservations=False, amount=5)
        start_date = '6'
        end_date = '7'
        response = self.test_client.get('/reservation/?page=notvalid&start_date=%s&end_date=%s' % (start_date, end_date), **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.context['reservations'].number, 1)
        self.assertEqual(response.context['has_reservations'], True)
        self.assertEqual(len(response.context['reservations']), len(self.reservations))
        self.assertEqual(response.context['client'], self.company)
        self.assertEqual(response.context['search_terms'], "")
        self.assertEqual(response.context['start_date'], start_date)
        self.assertEqual(response.context['end_date'], end_date)
        self.assertEqual(response.context['show_past'], False)
        self.assertEqual(response.context['show_confirmation'], None)
        self.assertEqual(response.context['confirmation_message'], None)
        self.assertEqual(response.context['has_past_reservations'], False)
    
    def test_search_variables_not_valid_trips(self):
        self.tearDown()
        self.setUp_for_trips()
        self.test_search_variables_not_valid()
    
    def test_confirmation_message(self):
        self.reservations = create_reservations(self.company, create_past_reservations=False, amount=5)
        show_confirmation = True
        confirmation_message = "The confirmation message"
        session = self.test_client.session
        session['show_confirmation'] = show_confirmation
        session['confirmation_message'] = confirmation_message
        session.save()
        response = self.test_client.get('/reservation/', **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.context['reservations'].number, 1)
        self.assertEqual(response.context['has_reservations'], True)
        self.assertEqual(len(response.context['reservations']), len(self.reservations))
        self.assertEqual(response.context['client'], self.company)
        self.assertEqual(response.context['search_terms'], "")
        self.assertEqual(response.context['start_date'], "")
        self.assertEqual(response.context['end_date'], "")
        self.assertEqual(response.context['show_past'], False)
        self.assertEqual(response.context['show_confirmation'], show_confirmation)
        self.assertEqual(response.context['confirmation_message'], confirmation_message)
        self.assertEqual(response.context['has_past_reservations'], False)
        
        show_confirmation = False
        confirmation_message = ""
        session = self.test_client.session
        session['show_confirmation'] = show_confirmation
        session['confirmation_message'] = confirmation_message
        session.save()
        response = self.test_client.get('/reservation/', **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.context['reservations'].number, 1)
        self.assertEqual(response.context['has_reservations'], True)
        self.assertEqual(len(response.context['reservations']), len(self.reservations))
        self.assertEqual(response.context['client'], self.company)
        self.assertEqual(response.context['search_terms'], "")
        self.assertEqual(response.context['start_date'], "")
        self.assertEqual(response.context['end_date'], "")
        self.assertEqual(response.context['show_past'], False)
        self.assertEqual(response.context['show_confirmation'], show_confirmation)
        self.assertEqual(response.context['confirmation_message'], confirmation_message)
        self.assertEqual(response.context['has_past_reservations'], False)
        
    def test_confirmation_message_trips(self):
        self.tearDown()
        self.setUp_for_trips()
        self.test_confirmation_message()
    
    def test_login_required(self):
        self.reservations = create_reservations(self.company, create_past_reservations=False, amount=5)
        test_login_required_base(self, '/reservation/')
        
    def test_login_required_trips(self):
        self.tearDown()
        self.setUp_for_trips()
        self.test_login_required()
    
    def test_search_variables_valid(self):
        self.reservations = create_reservations(self.company, create_past_reservations=False, amount=5)
        start_date = datetime.utcnow().date() + timedelta(days=1)
        end_date = datetime.utcnow().date() + timedelta(days=4)
        reservations = [reservation for reservation in self.reservations
                        if(start_date <= reservation.reservation_datetime.date() < end_date)]
        
        response = self.test_client.get('/reservation/?page=1&start_date=%s&end_date=%s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.context['reservations'].number, 1)
        self.assertEqual(response.context['has_reservations'], True)
        self.assertEqual(len(response.context['reservations']), len(reservations))
        self.assertEqual(response.context['client'], self.company)
        self.assertEqual(response.context['search_terms'], "")
        self.assertEqual(response.context['start_date'], start_date.strftime('%m/%d/%Y'))
        self.assertEqual(response.context['end_date'], end_date.strftime('%m/%d/%Y'))
        self.assertEqual(response.context['show_past'], False)
        self.assertEqual(response.context['show_confirmation'], None)
        self.assertEqual(response.context['confirmation_message'], None)
        self.assertEqual(response.context['has_past_reservations'], False)
    
    def test_search_variables_valid_trips(self):
        self.tearDown()
        self.setUp_for_trips()
        self.test_search_variables_valid()
    