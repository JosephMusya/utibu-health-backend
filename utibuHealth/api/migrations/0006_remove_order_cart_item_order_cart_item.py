# Generated by Django 5.0.3 on 2024-03-30 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_cartitem_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='order',
            name='cart_item',
            field=models.ManyToManyField(related_name='orders', to='api.cartitem'),
        ),
    ]