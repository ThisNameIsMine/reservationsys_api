# Generated by Django 4.2.7 on 2023-12-11 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_lesson_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]