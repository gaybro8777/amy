# Generated by Django 2.2.10 on 2020-05-01 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrequests', '0019_auto_20200413_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopinquiryrequest',
            name='user_notes',
            field=models.TextField(blank=True, help_text='Knowing if this workshop is on-line or in-person will help ensure we can best support you in coordinating the event.', verbose_name='Will this workshop be conducted in-person or online? Is there any other information you would like to share with us?'),
        ),
    ]
