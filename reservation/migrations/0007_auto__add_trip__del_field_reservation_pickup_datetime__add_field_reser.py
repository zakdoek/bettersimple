# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trip'
        db.create_table('reservation_trip', (
            ('reservation_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reservation.Reservation'], unique=True, primary_key=True)),
            ('trip_pickup_address', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Trip_pickup_address', unique=True, to=orm['reservation.Address'])),
            ('trip_dropoff_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 5, 0, 0))),
            ('trip_dropoff_address', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Trip_dropoff_address', unique=True, to=orm['reservation.Address'])),
        ))
        db.send_create_signal('reservation', ['Trip'])

        # Deleting field 'Reservation.pickup_datetime'
        db.rename_column('reservation_reservation', 'pickup_datetime', 'reservation_datetime')
                
#from datetime import *
#from reservation.models import *
#reservations = Reservation.objects.all()

#for reservation in reservations:
#    try:
#        if reservation.trip:
#            pass
#    except:
#        trip = Trip()
#        trip.reservation_datetime = reservation.reservation_datetime
#        trip.trip_dropoff_address = reservation.dropoff_address
#        trip.trip_dropoff_datetime = reservation.dropoff_datetime
#        trip.trip_pickup_address = reservation.pickup_address
#        trip.pickup_address = reservation.pickup_address
#        trip.dropoff_datetime = reservation.dropoff_datetime
#        trip.dropoff_address = reservation.dropoff_address
#        trip.customer = reservation.customer
#        trip.company = reservation.company
#        trip.passengers = reservation.passengers
#        reservation.delete()
#        trip.save()


    def backwards(self, orm):
        # Deleting model 'Trip'
        db.delete_table('reservation_trip')

        # Adding field 'Reservation.pickup_datetime'
        db.rename_column('reservation_reservation', 'reservation_datetime', 'pickup_datetime')


    models = {
        'charge.clientchargeprofile': {
            'Meta': {'object_name': 'ClientChargeProfile'},
            'charge_per_reservation': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '5', 'decimal_places': '2'}),
            'free_reservations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'clientservice.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'charge_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['charge.ClientChargeProfile']", 'unique': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'client_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'client_phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landmarks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reservation.Landmark']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'timezone_name': ('django.db.models.fields.CharField', [], {'default': "'US/Mountain'", 'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'e1f2bdbe-ed30-40b4-a243-1719ec7c2ea4'", 'max_length': '36'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'reservation.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landmark_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'reservation.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13'})
        },
        'reservation.landmark': {
            'Meta': {'object_name': 'Landmark'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reservation.Address']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'reservation.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reservation.Contact']"}),
            'customer_created': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dropoff_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Reservation_dropoff_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'dropoff_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 5, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'passengers': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pickup_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Reservation_pickup_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'reservation_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 5, 0, 0)'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'ccc315b8-a0e1-41be-ba10-1cb49f7605c9'", 'max_length': '36'})
        },
        'reservation.trip': {
            'Meta': {'object_name': 'Trip', '_ormbases': ['reservation.Reservation']},
            'reservation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reservation.Reservation']", 'unique': 'True', 'primary_key': 'True'}),
            'trip_dropoff_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Trip_dropoff_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'trip_dropoff_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 5, 0, 0)'}),
            'trip_pickup_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Trip_pickup_address'", 'unique': 'True', 'to': "orm['reservation.Address']"})
        }
    }

    complete_apps = ['reservation']
