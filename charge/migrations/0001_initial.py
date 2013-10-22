# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClientChargeProfile'
        db.create_table('charge_clientchargeprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('free_reservations', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('charge_per_reservation', self.gf('django.db.models.fields.DecimalField')(default=1.0, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('charge', ['ClientChargeProfile'])

        # Adding model 'MonthlyCharge'
        db.create_table('charge_monthlycharge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clientservice.Client'])),
            ('charge_date', self.gf('django.db.models.fields.DateField')()),
            ('charge_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discount_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
        ))
        db.send_create_signal('charge', ['MonthlyCharge'])

        # Adding model 'ReservationCharge'
        db.create_table('charge_reservationcharge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monthly_charge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['charge.MonthlyCharge'])),
            ('reservation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reservation.Reservation'])),
        ))
        db.send_create_signal('charge', ['ReservationCharge'])


    def backwards(self, orm):
        # Deleting model 'ClientChargeProfile'
        db.delete_table('charge_clientchargeprofile')

        # Deleting model 'MonthlyCharge'
        db.delete_table('charge_monthlycharge')

        # Deleting model 'ReservationCharge'
        db.delete_table('charge_reservationcharge')


    models = {
        'charge.clientchargeprofile': {
            'Meta': {'object_name': 'ClientChargeProfile'},
            'charge_per_reservation': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '5', 'decimal_places': '2'}),
            'free_reservations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'charge.monthlycharge': {
            'Meta': {'object_name': 'MonthlyCharge'},
            'charge_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'charge_date': ('django.db.models.fields.DateField', [], {}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']"}),
            'discount_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'charge.reservationcharge': {
            'Meta': {'object_name': 'ReservationCharge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_charge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['charge.MonthlyCharge']"}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reservation.Reservation']"})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'0506f2cd-c91c-4d60-a518-3fd577eb2a76'", 'max_length': '36'}),
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
            'dropoff_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Reservation_dropoff_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'dropoff_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 28, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'passengers': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pickup_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Reservation_pickup_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'pickup_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 28, 0, 0)'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'c88f889e-646f-4102-87c7-e85c8da65304'", 'max_length': '36'})
        }
    }

    complete_apps = ['charge']