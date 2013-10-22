from django.contrib.auth.models import User
from django.test import client
from reservation.models import *
from clientservice.models import *
from charge.models import *
from reservation import types

def create_company(use_passengers=False, use_special_instructions=False, reservation_type=types.APPOINTMENT, use_text_message_reminders=False):
    username = 'testuser'
    password = 'password'
    user = User.objects.create_user(username, 'test@test.com', password)
    user.save()
    company = Client()
    company.name = "Test Company"
    company.address = "123 Test Drive"
    company.city = "Fort Collins"
    company.state = "CO"
    company.zipcode = "80526"
    company.client_phone = "1234567890"
    company.client_email = "client@test.com"
    company.contact_phone = "1234567890"
    company.contact_email = "contact@test.com"
    company.charge_profile = ClientChargeProfile.objects.create()
    company.industry_profile = IndustryProfile.objects.create()
    company.industry_profile.use_passengers = use_passengers
    company.industry_profile.use_special_instructions = use_special_instructions
    company.industry_profile.use_text_message_reminders = use_text_message_reminders
    company.industry_profile.use_special_instructions = use_special_instructions
    company.industry_profile.reservation_type = reservation_type
    company.industry_profile.save()
    company.save()
    profile = UserProfile()
    profile.client = company
    profile.user = user
    profile.save()
    return (username, password, user, company)

def create_reservations(company, create_past_reservations=False, amount=5):
    reservations = []
    for i in ( range(-1* amount, amount) if create_past_reservations else range(amount) ):
        reservations.append(create_reservation(company, i))
    return reservations

def create_reservation(company, index):
    # If other types are created, then this will have to change.
    reservation = Reservation() if company.industry_profile.reservation_type == types.APPOINTMENT else Trip()
    reservation.reservation_datetime = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=2+index)
    customer = Contact()
    customer.name = "Test Customer %s" % index
    customer.email = "test@test.com"
    customer.phone = "0987654321"
    customer.save()
    reservation.customer = customer
    reservation.company = company
    reservation.passengers = (1+index) if company.industry_profile.use_passengers else 1
    reservation.special_instructions = "Special Instructions for %s" % index if company.industry_profile.use_special_instructions else ""
    reservation.send_reminder_text = company.industry_profile.use_text_message_reminders
    if company.industry_profile.reservation_type == types.TRIP:
        reservation.pickup_address = Address.objects.create()
        reservation.pickup_address.landmark_name = ""
        reservation.pickup_address.address = "123%s Test Drive"
        reservation.pickup_address.city = "Fort Collins"
        reservation.pickup_address.state = "CO"
        reservation.pickup_address.zipcode = "80526"
        reservation.pickup_address.save()
        reservation.dropoff_address = Address.objects.create()
        reservation.dropoff_address.landmark_name = ""
        reservation.dropoff_address.address = "123%s Test Drive"
        reservation.dropoff_address.city = "Watertown"
        reservation.dropoff_address.state = "WI"
        reservation.dropoff_address.zipcode = "53098"
        reservation.dropoff_address.save()
    reservation.save()
    return reservation
    

def test_login_required_base(test_runner, path):
    test_runner.test_client.logout()
    response = test_runner.test_client.get(path, follow=True)
    test_runner.assertEqual(3, len(response.redirect_chain), "the redirect chain for viewing a page that login is required is invalid.")
    test_runner.assertTrue(response.redirect_chain[1][0].find('accounts/login?next='+path) > -1)
    test_runner.assertTrue(response.redirect_chain[2][0].find('accounts/login/?next=') > -1)