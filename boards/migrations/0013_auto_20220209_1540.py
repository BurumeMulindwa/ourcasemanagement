# Generated by Django 3.2.8 on 2022-02-09 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0012_topic_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='deadline',
            field=models.CharField(choices=[('3 Days', '3 days'), ('30 days', '30 days'), ('60 days', '60 days'), ('90 days', '90 days'), ('120 days', '120 days'), ('180 days', '180 days'), ('360 days', '360 days')], default='3 Days', max_length=35),
        ),
        migrations.AlterField(
            model_name='topic',
            name='progress',
            field=models.CharField(choices=[('Acknowledgement sent', 'Acknowledgement sent'), ('Case rejected', 'Case rejected'), ('Interim report sent', 'Interim report sent'), ('Allocated to SRC Department', 'Allocated to SRC Department'), ('Allocated to Third Party', 'Allocated to Third Party'), ('Partial / Interim Response sent', 'Partial / Interim Response sent'), ('Final Response sent', 'Final Response sent'), ('Partial / Interim Response Received', 'Partial / Interim Response Received'), ('Final Response Received', 'Final Response Received'), ('Case Finalised', 'Case Finalised')], default='3 Days', max_length=40),
        ),
    ]
