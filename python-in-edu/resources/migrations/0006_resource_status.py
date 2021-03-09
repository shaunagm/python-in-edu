# Generated by Django 3.1.6 on 2021-03-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0005_auto_20210301_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='status',
            field=models.CharField(choices=[('PR', 'Proposed'), ('AC', 'Accepted'), ('RJ', 'Rejected'), ('WD', 'Withdrawn')], default='PR', max_length=3),
        ),
    ]