# Generated by Django 2.2.8 on 2019-12-17 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kd', '0116_lotsman_documents_hierarcy_files'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lotsman_documents_hierarcy_files',
            unique_together={('lotsman_document', 'path')},
        ),
    ]
