# forms.py
from django import forms
from .models import StreetRoadInformation, PropertyInformation
from .data import DIVISION_CHOICES, WARD_CHOICES, CELL_CHOICES

class StreetRoadInformationForm(forms.ModelForm):
    class Meta:
        model = StreetRoadInformation
        fields = '__all__'
        widgets = {
            'street_road_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'village': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'street_road_name_signage': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'starting_point': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'ending_point': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'pedestrian_walkway_status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'cctv_infrastructure': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'division': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'ward': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'cell': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'area_councilor_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'area_councilor_phone_no': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'road_surface_condition': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'starting_coordinates': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'ending_coordinates': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'street_road_distance': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'no_properties_on_street': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'street_lighting_status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'drainage_system': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'service_lane_existence': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initial values for all choices
        self.fields['division'].choices = DIVISION_CHOICES
        self.fields['ward'].choices = WARD_CHOICES
        self.fields['cell'].choices = CELL_CHOICES

        # Dynamic filtering based on instance (editing existing object)
        if self.instance and self.instance.division:
            self.fields['ward'].choices = self.get_ward_choices(self.instance.division)
            if self.instance.ward:
                self.fields['cell'].choices = self.get_cell_choices(self.instance.ward)

    def get_ward_choices(self, division):
        """Return filtered ward choices based on division."""
        if division == 'South_Division':
            return [
                ('Kakoba Ward', 'Kakoba Ward'),
                ('Nyamityobora Ward', 'Nyamityobora Ward'),
                ('Katete Ward', 'Katete Ward'),
                ('Ruti Ward', 'Ruti Ward'),
                ('Bugashe Ward', 'Bugashe Ward'),
                ('Katojo Ward', 'Katojo Ward'),
            ]
        elif division == 'North_Division':
            return [
                ('Rwenjeru Ward', 'Rwenjeru Ward'),
                ('Nyabuhama Ward', 'Nyabuhama Ward'),
                ('Biharwe East Ward', 'Biharwe East Ward'),
                ('Biharwe West Ward', 'Biharwe West Ward'),
                ('Kishasha Ward', 'Kishasha Ward'),
                ('Kamukuzi Ward', 'Kamukuzi Ward'),
                ('Ruharo Ward', 'Ruharo Ward'),
                ('Kakiika Ward', 'Kakiika Ward'),
                ('Rwemigina Ward', 'Rwemigina Ward'),
            ]
        return []

    def get_cell_choices(self, ward):
        """Return filtered cell choices based on ward."""
        cell_dict = {
            'Kakoba Ward': [
                ('Kakoba Central', 'Kakoba Central'),
                ('Kakoba Quarters', 'Kakoba Quarters'),
                ('Kihindi', 'Kihindi'),
                ('Kisenyi A', 'Kisenyi A'),
                ('Kishwahili', 'Kishwahili'),
                ('Kyapotani', 'Kyapotani'),
                ('Lugazi', 'Lugazi'),
                ('N.T.C', 'N.T.C'),
                ('Nyakaizi', 'Nyakaizi'),
                ('Police/Prisons', 'Police/Prisons'),
                ('Rwentondo', 'Rwentondo'),
                ('Mandela', 'Mandela'),
            ],
            'Nyamityobora Ward': [
                ('Agip', 'Agip'),
                ('Central', 'Central'),
                ('Kabateraine', 'Kabateraine'),
                ('Kilembe', 'Kilembe'),
                ('Lower', 'Lower'),
                ('Lubiri', 'Lubiri'),
                ('Market', 'Market'),
                ('Muti', 'Muti'),
                ('Survey', 'Survey'),
                ('Upper', 'Upper'),
            ],
            'Katete Ward': [
                ('Bihunya', 'Bihunya'),
                ('Karugangama', 'Karugangama'),
                ('Katete Central', 'Katete Central'),
                ('Kitebero', 'Kitebero'),
                ('Nsikye', 'Nsikye'),
                ('Nyamitanga', 'Nyamitanga'),
                ('Rwemirinzi', 'Rwemirinzi'),
                ('Rwizi', 'Rwizi'),
            ],
            'Ruti Ward': [
                ('Kafunda', 'Kafunda'),
                ('Kateera', 'Kateera'),
                ('Kirehe', 'Kirehe'),
                ('Market', 'Market'),
                ('Nsikye', 'Nsikye'),
                ('Nyamitanga', 'Nyamitanga'),
                ('Rwizi', 'Rwizi'),
                ('Tankhill', 'Tankhill'),
            ],
            'Bugashe Ward': [
                ('Bugashe', 'Bugashe'),
                ('Kanyamurimi', 'Kanyamurimi'),
                ('Kibaya I', 'Kibaya I'),
                ('Kibaya II', 'Kibaya II'),
                ('Kibona', 'Kibona'),
                ('Nyakahanga', 'Nyakahanga'),
                ('Rutooma', 'Rutooma'),
            ],
            'Katojo Ward': [
                ('Karugyembe', 'Karugyembe'),
                ('Kitojo', 'Kitojo'),
                ('Kibingo', 'Kibingo'),
                ('Kitagata', 'Kitagata'),
                ('Kitooma', 'Kitooma'),
                ('Ngaara', 'Ngaara'),
                ('Nyakashambya', 'Nyakashambya'),
                ('Rwariire I', 'Rwariire I'),
                ('Rwariire II', 'Rwariire II'),
                ('Rwemigina', 'Rwemigina'),
                ('Rwentondo', 'Rwentondo'),
            ],
            'Rwenjeru Ward': [
                ('Rwendama', 'Rwendama'),
                ('Rwenjeru South', 'Rwenjeru South'),
                ('Kamatarisi', 'Kamatarisi'),
                ('Kabucebebe', 'Kabucebebe'),
                ('Rwakaterere', 'Rwakaterere'),
                ('Rwenjeru North', 'Rwenjeru North'),
                ('Katengyeto', 'Katengyeto'),
                ('Katerananga', 'Katerananga'),
                ('Akaku/Rwenjeru Wd', 'Akaku/Rwenjeru Wd'),
            ],
            'Nyabuhama Ward': [
                ('Ekigando', 'Ekigando'),
                ('Nyaruhanga', 'Nyaruhanga'),
                ('Katojo', 'Katojo'),
                ('Rugarama', 'Rugarama'),
                ('Kakukuru', 'Kakukuru'),
                ('Rwebishekye', 'Rwebishekye'),
            ],
            'Biharwe East Ward': [
                ('Kyanyarukondo 1', 'Kyanyarukondo 1'),
                ('Rwemirabyo', 'Rwemirabyo'),
                ('Rwenkanja', 'Rwenkanja'),
                ('Kasharara', 'Kasharara'),
            ],
            'Biharwe West Ward': [
                ('Biharwe East', 'Biharwe East'),
                ('Biharwe Central 11', 'Biharwe Central 11'),
                ('Kyanyarukondo 11', 'Kyanyarukondo 11'),
                ('Ekihangire', 'Ekihangire'),
                ('Mailo', 'Mailo'),
                ('Biharwe West', 'Biharwe West'),
                ('Biharwe Central 1', 'Biharwe Central 1'),
                ('Kanyara', 'Kanyara'),
            ],
            'Kishasha Ward': [
                ('Kyempitsi', 'Kyempitsi'),
                ('Kinyaza', 'Kinyaza'),
                ('Nyakanengo', 'Nyakanengo'),
                ('Rwabukwire', 'Rwabukwire'),
                ('Rwobuyenje North', 'Rwobuyenje North'),
                ('Kibungo', 'Kibungo'),
                ('Rwobuyenje West', 'Rwobuyenje West'),
                ('Nyamabare', 'Nyamabare'),
            ],
            'Kamukuzi Ward': [
                ('Biafra Cell', 'Biafra Cell'),
                ('Boma Cell', 'Boma Cell'),
                ('Kakiika Cell', 'Kakiika Cell'),
                ('Kakyeka Cell', 'Kakyeka Cell'),
                ('Kamukuzi Cell', 'Kamukuzi Cell'),
                ('Kashanyarazi Cell', 'Kashanyarazi Cell'),
                ('Medical Cell', 'Medical Cell'),
                ('Ntare Cell', 'Ntare Cell'),
                ('Rwebikoona Cell', 'Rwebikoona Cell'),
            ],
            'Ruharo Ward': [
                ('Kiyanja Cell', 'Kiyanja Cell'),
                ('Mbaguta Cell', 'Mbaguta Cell'),
                ('Mbarara High School', 'Mbarara High School'),
                ('Nkokonjeru Cell', 'Nkokonjeru Cell'),
                ('Rwizi Cell', 'Rwizi Cell'),
            ],
            'Kakiika Ward': [
                ('Makenke Cell', 'Makenke Cell'),
                ('Nyakabungo Cell', 'Nyakabungo Cell'),
                ('Nyakiziba Cell', 'Nyakiziba Cell'),
                ('Butagatsi Cell', 'Butagatsi Cell'),
                ('Kacence East Cell', 'Kacence East Cell'),
                ('Kacence West Cell', 'Kacence West Cell'),
                ('Rwobuyenje Cell', 'Rwobuyenje Cell'),
            ],
            'Rwemigina Ward': [
                ('Rwemigina Central Cell', 'Rwemigina Central Cell'),
                ('Kabingo Cell', 'Kabingo Cell'),
                ('Rwebiihuro Cell', 'Rwebiihuro Cell'),
                ('Buremba I Cell', 'Buremba I Cell'),
                ('Buremba II Cell', 'Buremba II Cell'),
                ('Kenkombe Cell', 'Kenkombe Cell'),
            ],
        }
        return cell_dict.get(ward, [])


class PropertyInformationForm(forms.ModelForm):
    class Meta:
        model = PropertyInformation
        fields = '__all__'
        widgets = {
            'property_no': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'street': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'property_number_plate': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'development_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'fencing_gate_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'property_usage': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'road_reserve_minimum': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'coordinates': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'no_units_on_property': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'no_users_occupants': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'owner_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'owner_phone_no': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
        }