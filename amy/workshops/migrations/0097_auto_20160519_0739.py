# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 12:39
from __future__ import unicode_literals

import json

from django.db import migrations, models


def populate_languages(apps, schema_editor):
    """Populate the Languages table.

    [1] lists IANA as the registry maintainer, [2] looks like that
    registry, and the JSON serialized registry is borrowed from [3].

    [1]: https://tools.ietf.org/html/rfc5646#section-2.2.1
    [2]: http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
    [3]: https://github.com/mattcg/language-subtag-registry/
    """
    with open('data/registry.json', encoding='utf-8') as f:
        languages = json.load(f)

    Language = apps.get_model('workshops', 'Language')
    for language in languages:
        if language['Type'] == 'language' and len(language['Subtag']) <= 2:
            # skip others until we need them
            # https://github.com/swcarpentry/amy/issues/582#issuecomment-159506884
            Language.objects.get_or_create(
                name=' '.join(language['Description'])[:40],
                subtag=language['Subtag']
            )


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0096_change_help_text_in_training_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Description of this language tag in English', max_length=40)),
                ('subtag', models.CharField(help_text='Primary language subtag.  https://tools.ietf.org/html/rfc5646#section-2.2.1', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='languages',
            field=models.ManyToManyField(blank=True, to='workshops.Language'),
        ),
        migrations.RunPython(populate_languages),
    ]
