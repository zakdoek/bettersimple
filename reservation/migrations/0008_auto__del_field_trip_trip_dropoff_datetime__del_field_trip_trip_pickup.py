# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Trip.trip_dropoff_datetime'
        db.rename_column('reservation_trip', 'trip_dropoff_datetime', 'dropoff_datetime')

        # Deleting field 'Trip.trip_pickup_address'
        db.rename_column('reservation_trip', 'trip_pickup_address_id', 'pickup_address_id')

        # Deleting field 'Trip.trip_dropoff_address'
        db.rename_column('reservation_trip', 'trip_dropoff_address_id', 'dropoff_address_id')

        # Deleting field 'Reservation.dropoff_datetime'
        db.delete_column('reservation_reservation', 'dropoff_datetime')

        # Deleting field 'Reservation.pickup_address'
        db.delete_column('reservation_reservation', 'pickup_address_id')

        # Deleting field 'Reservation.dropoff_address'
        db.delete_column('reservation_reservation', 'dropoff_address_id')


    def backwards(self, orm):
        # Adding field 'Trip.trip_dropoff_datetime'
        db.rename_column('reservation_trip', 'dropoff_datetime', 'trip_dropoff_datetime')

        # Deleting field 'Trip.trip_pickup_address'
        db.rename_column('reservation_trip', 'pickup_address_id', 'trip_pickup_address_id')

        # Deleting field 'Trip.trip_dropoff_address'
        db.rename_column('reservation_trip', 'dropoff_address_id', 'trip_dropoff_address_id')

        # Adding field 'Reservation.dropoff_datetime'
        db.add_column('reservation_reservation', 'dropoff_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 5, 0, 0)),
                      keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Reservation.pickup_address'
        raise RuntimeError("Cannot reverse this migration. 'Reservation.pickup_address' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Reservation.dropoff_address'
        raise RuntimeError("Cannot reverse this migration. 'Reservation.dropoff_address' and its values cannot be restored.")

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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'febd5b79-b7fa-4d3e-9528-07a3c33b90d3'", 'max_length': '36'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'passengers': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'reservation_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 5, 0, 0)'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'14b2adb6-c70e-49d4-9c16-3be50987c73e'", 'max_length': '36'})
        },
        'reservation.trip': {
            'Meta': {'object_name': 'Trip', '_ormbases': ['reservation.Reservation']},
            'dropoff_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Trip_dropoff_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'dropoff_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 5, 0, 0)'}),
            'pickup_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Trip_pickup_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'reservation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reservation.Reservation']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['reservation']
