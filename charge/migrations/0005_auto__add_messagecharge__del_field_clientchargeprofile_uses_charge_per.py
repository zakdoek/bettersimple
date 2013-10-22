# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MessageCharge'
        db.create_table('charge_messagecharge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monthly_charge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['charge.MonthlyCharge'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message.Message'])),
        ))
        db.send_create_signal('charge', ['MessageCharge'])

        # Deleting field 'ClientChargeProfile.uses_charge_per_month'
        db.delete_column('charge_clientchargeprofile', 'uses_charge_per_month')

        # Adding field 'ClientChargeProfile.charge_per_message'
        db.add_column('charge_clientchargeprofile', 'charge_per_message',
                      self.gf('django.db.models.fields.DecimalField')(default=0.02, max_digits=5, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'MessageCharge'
        db.delete_table('charge_messagecharge')

        # Adding field 'ClientChargeProfile.uses_charge_per_month'
        db.add_column('charge_clientchargeprofile', 'uses_charge_per_month',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'ClientChargeProfile.charge_per_message'
        db.delete_column('charge_clientchargeprofile', 'charge_per_message')


    models = {
        'charge.clientchargeprofile': {
            'Meta': {'object_name': 'ClientChargeProfile'},
            'charge_per_message': ('django.db.models.fields.DecimalField', [], {'default': '0.02', 'max_digits': '5', 'decimal_places': '2'}),
            'charge_per_month': ('django.db.models.fields.DecimalField', [], {'default': '20.0', 'max_digits': '6', 'decimal_places': '2'}),
            'charge_per_reservation': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '5', 'decimal_places': '2'}),
            'free_reservations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'charge.messagecharge': {
            'Meta': {'object_name': 'MessageCharge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['message.Message']"}),
            'monthly_charge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['charge.MonthlyCharge']"})
        },
        'charge.monthlycharge': {
            'Meta': {'object_name': 'MonthlyCharge'},
            'charge_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'charge_date': ('django.db.models.fields.DateField', [], {}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']"}),
            'discount_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stripe_charge_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
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
            'industry_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clientservice.IndustryProfile']", 'unique': 'True'}),
            'landmarks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reservation.ClientLandmark']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'timezone_name': ('django.db.models.fields.CharField', [], {'default': "'US/Mountain'", 'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'8cbd4dc4-4dd7-418b-bc26-998346ad5d8d'", 'max_length': '36'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'clientservice.industryprofile': {
            'Meta': {'object_name': 'IndustryProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reservation_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'use_passengers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_special_instructions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_text_message_reminders': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'message.message': {
            'Meta': {'object_name': 'Message'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_type': ('django.db.models.fields.IntegerField', [], {}),
            'monthly_charge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['charge.MonthlyCharge']", 'null': 'True', 'blank': 'True'}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reservation.Reservation']", 'null': 'True', 'blank': 'True'}),
            'send_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 16, 0, 0)'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'reservation_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 17, 0, 0)'}),
            'special_instructions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'85fc2906-b700-4b45-8735-d8eb80f3bb92'", 'max_length': '36'})
        }
    }

    complete_apps = ['charge']