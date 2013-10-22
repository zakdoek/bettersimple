# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Landmark'
        db.delete_table('reservation_landmark')


    def backwards(self, orm):
        # Adding model 'Landmark'
        db.create_table('reservation_landmark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reservation.Address'], unique=True)),
        ))
        db.send_create_signal('reservation', ['Landmark'])


    models = {
        'charge.clientchargeprofile': {
            'Meta': {'object_name': 'ClientChargeProfile'},
            'charge_per_month': ('django.db.models.fields.DecimalField', [], {'default': '20.0', 'max_digits': '6', 'decimal_places': '2'}),
            'charge_per_reservation': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '5', 'decimal_places': '2'}),
            'free_reservations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'uses_charge_per_month': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
            'industry_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clientservice.IndustryProfile']", 'unique': 'True'}),
            'landmarks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reservation.ClientLandmark']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'timezone_name': ('django.db.models.fields.CharField', [], {'default': "'US/Mountain'", 'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'27c870ee-8d1c-424f-8d48-21a5170a357f'", 'max_length': '36'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'clientservice.industryprofile': {
            'Meta': {'object_name': 'IndustryProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reservation_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'use_passengers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_special_instructions': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        'reservation.clientlandmark': {
            'Meta': {'object_name': 'ClientLandmark'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reservation.Address']", 'unique': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'reservation.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13'})
        },
        'reservation.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reservation.Contact']"}),
            'customer_created': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'passengers': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'reservation_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 14, 0, 0)'}),
            'special_instructions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'4cc4d93f-528f-4975-bce4-32b549dbc0e9'", 'max_length': '36'})
        },
        'reservation.trip': {
            'Meta': {'object_name': 'Trip', '_ormbases': ['reservation.Reservation']},
            'dropoff_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Trip_dropoff_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'dropoff_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 14, 0, 0)'}),
            'pickup_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Trip_pickup_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'reservation_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reservation.Reservation']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['reservation']