# Generated by Django 2.2.7 on 2019-11-24 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_auto_20191122_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='option_group',
            field=models.ForeignKey(blank=True, help_text='Select option group if using type "Option" or "Multi Option"', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='values_list', to='person.AttributeOptionGroup', verbose_name='Option Group'),
        ),
    ]
