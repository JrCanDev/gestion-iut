# Generated by Django 4.0.3 on 2022-04-20 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cour',
            name='td_promotion',
        ),
        migrations.AddField(
            model_name='cour',
            name='td_promotion',
            field=models.ManyToManyField(blank=True, related_name='td_promotion', to='management.tdpromotion'),
        ),
    ]
