# Generated by Django 3.0.2 on 2020-01-21 07:39

from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('planing', '0071_posting_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation_refs',
            name='income',
        ),
        migrations.RemoveField(
            model_name='operation_refs',
            name='outcome',
        ),
        migrations.AddField(
            model_name='operation_refs',
            name='child',
            field=isc_common.fields.related.ForeignKeyCascade(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='operation_child', to='planing.Operations'),
        ),
        migrations.AddField(
            model_name='operation_refs',
            name='parent',
            field=isc_common.fields.related.ForeignKeyCascade(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operation_parent', to='planing.Operations'),
        ),
    ]
