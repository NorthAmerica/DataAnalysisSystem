# Generated by Django 2.0.6 on 2018-06-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DAS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Txt_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(blank=True, max_length=255)),
                ('file_date', models.DateField()),
                ('file', models.FileField(upload_to='txt/')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
