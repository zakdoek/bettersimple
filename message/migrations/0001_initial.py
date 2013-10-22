# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('message_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reservation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reservation.Reservation'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('send_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 21, 0, 0))),
        ))
        db.send_create_signal('message', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('message_message')


    models = {
        'clientservice.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'69d7829d-596c-414a-bc20-8b5a50265d0f'", 'max_length': '36'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'message.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reservation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reservation.Reservation']"}),
            'send_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 21, 0, 0)'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
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
            'dropoff_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 21, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'passengers': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pickup_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Reservation_pickup_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'pickup_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 21, 0, 0)'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'8ec42443-d327-4853-85f7-22bf8ed856cf'", 'max_length': '36'})
        }
    }

    complete_apps = ['message']
