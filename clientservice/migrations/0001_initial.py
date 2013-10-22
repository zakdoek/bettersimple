# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('clientservice_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('client_phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('client_email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='5e0338bc-f046-49cd-b91d-26211cf54b09', max_length=36)),
        ))
        db.send_create_signal('clientservice', ['Client'])

        # Adding model 'ClientCode'
        db.create_table('clientservice_clientcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clientservice.Client'], unique=True)),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('head_code', self.gf('django.db.models.fields.TextField')()),
            ('link_code', self.gf('django.db.models.fields.TextField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('clientservice', ['ClientCode'])

        # Adding model 'UserProfile'
        db.create_table('clientservice_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clientservice.Client'])),
        ))
        db.send_create_signal('clientservice', ['UserProfile'])

        # Adding model 'PotentialClient'
        db.create_table('clientservice_potentialclient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
        ))
        db.send_create_signal('clientservice', ['PotentialClient'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('clientservice_client')

        # Deleting model 'ClientCode'
        db.delete_table('clientservice_clientcode')

        # Deleting model 'UserProfile'
        db.delete_table('clientservice_userprofile')

        # Deleting model 'PotentialClient'
        db.delete_table('clientservice_potentialclient')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'ef7b1021-1e24-40b0-81a3-937e72d45821'", 'max_length': '36'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'clientservice.clientcode': {
            'Meta': {'object_name': 'ClientCode'},
            'client': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clientservice.Client']", 'unique': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {}),
            'head_code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'link_code': ('django.db.models.fields.TextField', [], {})
        },
        'clientservice.potentialclient': {
            'Meta': {'object_name': 'PotentialClient'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'clientservice.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clientservice.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['clientservice']