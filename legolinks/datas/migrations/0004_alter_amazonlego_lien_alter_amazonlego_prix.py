# Generated by Django 4.1.4 on 2022-12-21 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datas', '0003_alter_productlego_nb_pieces'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonlego',
            name='lien',
            field=models.CharField(max_length=255, null=True, verbose_name='Lien'),
        ),
        migrations.AlterField(
            model_name='amazonlego',
            name='prix',
            field=models.FloatField(null=True, verbose_name='Dernier prix'),
        ),
    ]
