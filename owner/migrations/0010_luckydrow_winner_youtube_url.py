# Generated by Django 5.1.3 on 2024-12-18 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0009_luckydrow_winner_added_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='luckydrow_winner',
            name='youtube_url',
            field=models.CharField(default='', max_length=500),
        ),
    ]