from django.utils import unittest
from reservation.models import *
from clientservice.models import Client, IndustryProfile
from charge.models import ClientChargeProfile

class SharedTestCase(unittest.TestCase):
    """Tests the shared methods of the class"""
    def test_make_uuid(self):
        self.assertRegexpMatches(make_uuid(), "([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})", "make__uuid did not create a valid regex.")
        
    def test_escape(self):
        self.assertTrue(escape('1"A') == '1\\"A', "the escape function didn't work as expected")
        
    def test_round_to_base(self):
        self.assertTrue(round_to_base(2, 5, 10) == 0, "Rounding down didn't work.")
        self.assertTrue(round_to_base(3, 5, 10) == 5, "Rounding up didn't work.")
        self.assertTrue(round_to_base(2, 4, 10) == 4, "Rounding up at halfway point didn't work.")
        self.assertTrue(round_to_base(15, 5, 10) == 10, "Hitting the ceiling didn't work.")
        
class ContactTestCase(unittest.TestCase):
    """Tests the Contact model"""
    def setUp(self):
        self.contact_unicode = Contact.objects.create(name="name", email="email@email.com", phone="1234567890")
    
    def tearDown(self):
        self.contact_unicode.delete()
    
    def test_unicode_returns_email(self):
        """Tests that __unicode__ returns the email of the contact"""
        self.assertEqual("%s" % self.contact_unicode, self.contact_unicode.email, "The default value for Contact was not the email address")

class AddressTestCase(unittest.TestCase):
    """Tests the Address model"""
    def setUp(self):
        self.test_address = Address.objects.create(
                                                   landmark_name='landmark_name"',
                                                   address = 'address"',
                                                   city='city"',
                                                   state="WI",
                                                   zipcode="53098"
                                               )
    def tearDown(self):
        self.test_address.delete()
    
    def test_unicode(self):
        self.assertEqual(
                         "%s" % self.test_address,
                         "%s\t%s, %s  %s" % (self.test_address.address, self.test_address.city, self.test_address.state, self.test_address.zipcode),
                         "Unicode did not return the correct string."
                     )
    
    def test_address_string(self):
        self.assertEqual(
                         self.test_address.address_string(),
                         "%s\n%s\n%s, %s  %s" % (self.test_address.landmark_name, self.test_address.address, self.test_address.city, self.test_address.state, self.test_address.zipcode),
                         "address_string did not return the correct string."
                     )
    
        
    def test_json_string(self):
        self.assertEqual(
                         self.test_address.json_string(),
                         '{"landmark_name":"%s","address":"%s","city":"%s","state":"%s","zipcode":"%s"}' % (escape(self.test_address.landmark_name), escape(self.test_address.address), escape(self.test_address.city), escape(self.test_address.state), escape(self.test_address.zipcode)),
                         "json_string did not return the correct string."
                     )
    
    def test_uses_landmark(self):
        self.assertTrue(
                         self.test_address.uses_landmark(),
                         "The address says it's using a landmark"
                     )
        
    def test_contains(self):
        self.assertTrue(
                         self.test_address.contains(self.test_address.city),
                         "contains says it doesn't contain the city property of the address."
                     )
        self.assertTrue(
                         self.test_address.contains(self.test_address.city.upper()),
                         "contains says it doesn't contain the city property of the address when it's been capitalized."
                     )
        self.assertFalse(
                         self.test_address.contains("THERE'S NO WAY THIS EXISTS IN THE ADDRESS!"),
                         "contains said that a string that didn't exist did."
                     )

class ClientLandmarkTestCase(unittest.TestCase):
    """Tests the ClientLandmark model"""
    def setUp(self):
        self.address = Address.objects.create(
                                                   landmark_name='landmark_name',
                                                   address = 'address',
                                                   city='city',
                                                   state="WI",
                                                   zipcode="53098"
                                               )
        self.client = Client.objects.create(charge_profile=ClientChargeProfile.objects.create(), industry_profile=IndustryProfile.objects.create())
        self.landmark = ClientLandmark.objects.create(name=self.address.landmark_name, address=self.address, company=self.client)
    
    def tearDown(self):
        self.address.delete()
        self.client.delete()
        self.landmark.delete()
    
    def test_unicode(self):
        self.assertEqual(
                         "%s" % self.landmark,
                         self.landmark.name,
                         "Unicode did not return the name of the landmark."
                     )
    
    def test_select_option_string(self):
        self.assertEqual(
                         self.landmark.select_option_string(),
                         '<option value="%s">%s</option>' % (self.landmark.id, self.landmark.name),
                         "The html code for the option was not returned correctly."
                     )
    
    def test_html(self):
        self.assertEqual(
                         self.landmark.html(),
                         '''
<address>
<strong>%s</strong><br>
%s<br>
%s, %s  %s
</address>
''' % (self.landmark.name, self.landmark.address.address, self.landmark.address.city, self.landmark.address.state, self.landmark.address.zipcode),
                         "The html code was not returned correctly."
                     )
        
class ActiveReservationManagerTestCase(unittest.TestCase):
    """Tests the ActiveReservationManager class"""
    def setUp(self):
        self.contact = Contact.objects.create(name="name", email="email@email.com", phone="1234567890")
        self.company = Client.objects.create(charge_profile=ClientChargeProfile.objects.create(), industry_profile=IndustryProfile.objects.create())
        self.reservation_active = Reservation.objects.create(company=self.company, customer=self.contact)
        self.reservation_deactive = Reservation.objects.create(company=self.company, customer=self.contact, deleted=True)
        self.trip_active = Trip.objects.create(
                      company=self.company, 
                      customer=self.contact, 
                      pickup_address=Address.objects.create(),
                      dropoff_address=Address.objects.create()
                  )
        self.trip_deactive = Trip.objects.create(
                      company=self.company, 
                      customer=self.contact, 
                      pickup_address=Address.objects.create(),
                      dropoff_address=Address.objects.create(),
                      deleted=True
                  )
    def tearDown(self):
        self.trip_active.delete()
        self.trip_deactive.delete()
        self.reservation_active.delete()
        self.reservation_deactive.delete()
        self.contact.delete()
        self.company.delete()
        
    def test_active_and_objects(self):
        self.assertEqual(Reservation.objects.all().count(), 4)
        self.assertEqual(Reservation.active.all().count(), 2)
        self.assertEqual(Trip.objects.all().count(), 2)
        self.assertEqual(Trip.active.all().count(), 1)

class ReservationTestCase(unittest.TestCase):
    """Tests the Reservation model"""
    def setUp(self):
        self.contact = Contact.objects.create(name="name", email="email@email.com", phone="1234567890")
        self.company = Client.objects.create(charge_profile=ClientChargeProfile.objects.create(), industry_profile=IndustryProfile.objects.create())
        self.reservation_active = Reservation.objects.create(
                                     company=self.company, 
                                     customer=self.contact, 
                                     reservation_datetime=(datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=2))
                                 )
        self.reservation_deactive = Reservation.objects.create(
                                     company=self.company, 
                                     customer=self.contact, 
                                     reservation_datetime=(datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(days=2))
                                 )
        self.reservation_deleted = Reservation.objects.create(
                                     company=self.company, 
                                     customer=self.contact, 
                                     reservation_datetime=(datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=2)),
                                     deleted=True
                                 )
    
    def tearDown(self):
        self.reservation_active.delete()
        self.reservation_deactive.delete()
        self.reservation_deleted.delete()
        self.contact.delete()
        self.company.delete()
    
    def test_editable(self):
        self.assertTrue(self.reservation_active.editable())
        self.assertFalse(self.reservation_deactive.editable())
        self.assertFalse(self.reservation_deleted.editable())
    
    def test_unicode(self):
        self.assertEqual(
                         "%s" % self.reservation_active,
                         "Appt for %s at %s for %s%s" % (self.reservation_active.customer, self.reservation_active.company.localize(self.reservation_active.reservation_datetime), self.reservation_active.company, " - deleted" if self.reservation_active.deleted else "")
                     )
        self.assertEqual(
                         "%s" % self.reservation_deleted,
                         "Appt for %s at %s for %s%s" % (self.reservation_deleted.customer, self.reservation_deleted.company.localize(self.reservation_deleted.reservation_datetime), self.reservation_deleted.company, " - deleted" if self.reservation_deleted.deleted else "")
                     )
    
    def test_csv_string(self):
        self.assertEqual(
                         self.reservation_active.csv_string(),
                         [self.company.localize(self.reservation_active.reservation_datetime).strftime("%m/%d/%Y %I:%M %p"), self.reservation_active.customer.name, self.reservation_active.customer.phone, self.reservation_active.customer.email, self.reservation_active.passengers, self.reservation_active.special_instructions,  self.reservation_active.company.localize(self.reservation_active.last_modified).strftime("%m/%d/%Y %I:%M %p")]
                 )
    
    def test_clean(self):
        try:
            self.reservation_deactive.clean()
            # this should never be executed
            self.assertTrue(False)
        except ValidationError:
            self.assertTrue(True)
        
        try:
            self.reservation_active.clean()
            # this should never be executed
            self.assertTrue(True)
        except ValidationError:
            self.assertTrue(False)
        

class TripTestCase(unittest.TestCase):
    """Tests the Trip model"""
    def setUp(self):
        self.contact = Contact.objects.create(name="name", email="email@email.com", phone="1234567890")
        self.company = Client.objects.create(charge_profile=ClientChargeProfile.objects.create(), industry_profile=IndustryProfile.objects.create())
        self.trip_active = Trip.objects.create(
                                     company=self.company, 
                                     customer=self.contact, 
                                     reservation_datetime=(datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=2)),
                                     pickup_address=Address.objects.create(),
                                     dropoff_address=Address.objects.create()
                                 )
        self.trip_deactive = Trip.objects.create(
                                     company=self.company, 
                                     customer=self.contact, 
                                     reservation_datetime=(datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(days=2)),
                                     pickup_address=Address.objects.create(),
                                     dropoff_address=Address.objects.create()
                                 )
        self.trip_deleted = Trip.objects.create(
                                     company=self.company, 
                                     customer=self.contact, 
                                     reservation_datetime=(datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=2)),
                                     deleted=True,
                                     pickup_address=Address.objects.create(),
                                     dropoff_address=Address.objects.create()
                                 )
    
    def tearDown(self):
        self.trip_active.delete()
        self.trip_deactive.delete()
        self.trip_deleted.delete()
        self.contact.delete()
        self.company.delete()
    
    def test_editable(self):
        self.assertTrue(self.trip_active.editable())
        self.assertFalse(self.trip_deactive.editable())
        self.assertFalse(self.trip_deleted.editable())
    
    def test_unicode(self):
        self.assertEqual(
                         "%s" % self.trip_active,
                         "Trip for %s at %s for %s%s" % (self.trip_active.customer, self.trip_active.company.localize(self.trip_active.reservation_datetime), self.trip_active.company, " - deleted" if self.trip_active.deleted else "")
                     )
        self.assertEqual(
                         "%s" % self.trip_deleted,
                         "Trip for %s at %s for %s%s" % (self.trip_deleted.customer, self.trip_deleted.company.localize(self.trip_deleted.reservation_datetime), self.trip_deleted.company, " - deleted" if self.trip_deleted.deleted else "")
                     )
    
    def test_csv_string(self):
        self.assertEqual(
                         self.trip_active.csv_string(),
                         [self.trip_active.company.localize(self.trip_active.reservation_datetime).strftime("%m/%d/%Y %I:%M %p"), self.trip_active.customer.name, self.trip_active.customer.phone, self.trip_active.customer.email, self.trip_active.pickup_address.landmark_name, self.trip_active.pickup_address.address, self.trip_active.pickup_address.city, self.trip_active.pickup_address.state, self.trip_active.pickup_address.zipcode, self.trip_active.dropoff_address.landmark_name, self.trip_active.dropoff_address.address, self.trip_active.dropoff_address.city, self.trip_active.dropoff_address.state, self.trip_active.dropoff_address.zipcode, self.trip_active.passengers, self.trip_active.special_instructions, self.trip_active.company.localize(self.trip_active.last_modified).strftime("%m/%d/%Y %I:%M %p")]
                 )
    
    def test_clean(self):
        try:
            self.trip_deactive.clean()
            # this should never be executed
            self.assertTrue(False)
        except ValidationError:
            self.assertTrue(True)
        
        try:
            self.trip_active.clean()
            # this should never be executed
            self.assertTrue(True)
        except ValidationError:
            self.assertTrue(False)
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    