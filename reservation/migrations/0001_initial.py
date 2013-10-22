# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table('reservation_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
        ))
        db.send_create_signal('reservation', ['Contact'])

        # Adding model 'Address'
        db.create_table('reservation_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('landmark', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('reservation', ['Address'])

        # Adding model 'Reservation'
        db.create_table('reservation_reservation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pickup_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 5, 0, 0))),
            ('pickup_address', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Reservation_pickup_address', unique=True, to=orm['reservation.Address'])),
            ('dropoff_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 5, 0, 0))),
            ('dropoff_address', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Reservation_dropoff_address', unique=True, to=orm['reservation.Address'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reservation.Contact'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='403396a0-44e2-4acd-82eb-34452e53730d', max_length=36)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clientservice.Client'])),
        ))
        db.send_create_signal('reservation', ['Reservation'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table('reservation_contact')

        # Deleting model 'Address'
        db.delete_table('reservation_address')

        # Deleting model 'Reservation'
        db.delete_table('reservation_reservation')


    models = {
        'clientservice.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'client_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'client_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'6b42dbc2-d70e-450e-aab0-347be3ce41cc'", 'max_length': '36'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'reservation.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landmark': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'reservation.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'reservation.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reservation.Contact']"}),
            'dropoff_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Reservation_dropoff_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'dropoff_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 5, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pickup_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Reservation_pickup_address'", 'unique': 'True', 'to': "orm['reservation.Address']"}),
            'pickup_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 5, 0, 0)'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'e1f877f8-6c65-4a70-a1d3-6fc9c2e8cc8d'", 'max_length': '36'})
        }
    }

    complete_apps = ['reservation']