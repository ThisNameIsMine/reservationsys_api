# Generated by Django 4.2.7 on 2023-12-20 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_promocode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promocode',
            old_name='status',
            new_name='used',
        ),
        migrations.AlterField(
            model_name='promocode',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
