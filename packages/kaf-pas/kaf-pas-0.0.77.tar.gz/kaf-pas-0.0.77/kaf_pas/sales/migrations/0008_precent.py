# Generated by Django 2.2.1 on 2019-05-16 16:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import isc_common.fields.code_field
import isc_common.fields.description_field
import isc_common.fields.name_field
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ckk', '0043_auto_20190516_1628'),
        ('sales', '0007_customer_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Precent',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('id_old', models.BigIntegerField(blank=True, null=True, verbose_name='Идентификатор старый')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('code', isc_common.fields.code_field.CodeField()),
                ('name', isc_common.fields.name_field.NameField()),
                ('description', isc_common.fields.description_field.DescriptionField()),
                ('status', isc_common.fields.related.ForeignKeyProtect(default=None, on_delete=django.db.models.deletion.PROTECT, to='ckk.Status')),
            ],
            options={
                'verbose_name': 'Распоряжение',
            },
        ),
    ]
