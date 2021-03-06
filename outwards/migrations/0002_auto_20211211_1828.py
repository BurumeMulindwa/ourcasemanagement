# Generated by Django 3.2.8 on 2021-12-11 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outwards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='legal_instrument',
        ),
        migrations.AddField(
            model_name='case',
            name='instrument',
            field=models.CharField(choices=[('Request for Information', 'Request for Information'), ('Automatic Exchange of Information', 'Automatic Exchange of Information'), ('Spontaneous Exchange of Information', 'Spontaneous Exchange of Information')], default='OECD Model Tax Convention', max_length=100),
        ),
        migrations.AlterField(
            model_name='case',
            name='progress',
            field=models.CharField(choices=[('Acknowledgement sent', 'Acknowledgement sent'), ('Case rejected', 'Case rejected'), ('Interim report sent', 'Interim report sent'), ('Allocated to SRC Department', 'Allocated to SRC Department'), ('Allocated to Third Party', 'Allocated to Third Party'), ('Partial / Interim Response sent', 'Partial / Interim Response sent'), ('Final Response sent', 'Final Response sent'), ('Partial / Interim Response Received', 'Partial / Interim Response Received'), ('Final Response Received', 'Final Response Received'), ('Case Finalised', 'Case Finalised')], default='OECD Model Tax Convention', max_length=40),
        ),
        migrations.AlterField(
            model_name='case',
            name='query',
            field=models.CharField(choices=[('Request for Information', 'Request for Information'), ('Automatic Exchange of Information', 'Automatic Exchange of Information'), ('Spontaneous Exchange of Information', 'Spontaneous Exchange of Information')], default='OECD Model Tax Convention', max_length=150),
        ),
    ]
