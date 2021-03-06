# Generated by Django 2.2.7 on 2020-03-13 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='行政编号')),
                ('name', models.CharField(max_length=20, verbose_name='行政区划名')),
                ('parent_id', models.CharField(max_length=20, verbose_name='上级行政编号')),
                ('type', models.IntegerField(default=0, verbose_name='行政等级')),
            ],
            options={
                'verbose_name': '行政区划',
                'verbose_name_plural': '行政区划',
            },
        ),
    ]
