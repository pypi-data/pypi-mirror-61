# Generated by Django 2.2 on 2019-04-14 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('isc_common', '0021_auto_20190414_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AlterField(
            model_name='history',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='params',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AlterField(
            model_name='params',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='user_permission',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AlterField(
            model_name='user_permission',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='usergroup_permission',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AlterField(
            model_name='usergroup_permission',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='widgets_trees',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления'),
        ),
        migrations.AlterField(
            model_name='widgets_trees',
            name='lastmodified',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление'),
        ),
    ]
