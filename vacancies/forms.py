from django import forms


class SortFilterForm(forms.Form):
    ordering_by_city = forms.ChoiceField(label=None, required=False, choices=[
        ('Все', 'Все города'),
        ('Киев', 'Киев'),
        ('Львов', 'Львов'),
        ('Харьков', 'Харьков'),
        ('удаленно', 'удаленно'),
        ('другие города', 'другие города'),
    ])
    ordering_by_site = forms.ChoiceField(label=None, required=False, choices=[
        ('Все сайты', 'Все сайты'),
        ('dou', 'jobs.dou.ua'),
        ('djinni', 'djinni.co'),
        ('rabota', 'rabota.ua'),
    ])

