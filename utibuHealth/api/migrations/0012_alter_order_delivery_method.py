# Generated by Django 5.0.3 on 2024-03-31 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(choices=[('Deliver to my address', 'Deliver to my address'), ('Pick from pharmacy', 'Pick from pharmacy')], default='Pick from pharmacy', max_length=200),
        ),
    ]
