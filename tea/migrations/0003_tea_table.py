# Generated by Django 5.1.3 on 2024-12-25 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0002_tea_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tea_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.CharField(max_length=100)),
                ('added_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]