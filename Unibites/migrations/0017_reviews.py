# Generated by Django 5.2 on 2025-05-10 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Unibites', '0016_order_orderdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('review', models.TextField(max_length=300)),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
                'db_table': 'reviews',
            },
        ),
    ]
