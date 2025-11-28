# forms.py
from django import forms

from .models import StreetRoadInformation, PropertyInformation, Concern
from .data import DIVISION_CHOICES, WARD_CHOICES, CELL_CHOICES


# ---------------------------------------
# Street / Road Information Form
# ---------------------------------------
class StreetRoadInformationForm(forms.ModelForm):
    class Meta:
        model = StreetRoadInformation
        fields = "__all__"
        widgets = {
            "street_road_name": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "village": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "street_road_name_signage": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "starting_point": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "ending_point": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "pedestrian_walkway_status": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "cctv_infrastructure": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "division": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "ward": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "cell": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "area_councilor_name": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "area_councilor_phone_no": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "road_surface_condition": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "starting_coordinates": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "ending_coordinates": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "street_road_distance": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "no_properties_on_street": forms.NumberInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "street_lighting_status": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "drainage_system": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "service_lane_existence": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 text-indigo-600 focus:ring-indigo-500 "
                    "border-gray-300 rounded"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add a blank "select" option at the top
        self.fields["division"].choices = [("", "Select division")] + list(
            DIVISION_CHOICES
        )
        self.fields["ward"].choices = [("", "Select ward")] + list(WARD_CHOICES)
        self.fields["cell"].choices = [("", "Select cell")] + list(CELL_CHOICES)

        # If form is being POSTed, use the submitted values
        data = self.data or None
        instance = self.instance if getattr(self, "instance", None) else None

        # Division → Ward dynamic filtering
        if data and "division" in data:
            division_value = data.get("division")
            self.fields["ward"].choices = [("", "Select ward")] + self.get_ward_choices(
                division_value
            )
            # When division changes, reset cell list
            self.fields["cell"].choices = [("", "Select cell")]
        elif instance and instance.pk and instance.division:
            self.fields["ward"].choices = [("", "Select ward")] + self.get_ward_choices(
                instance.division
            )
            if instance.ward:
                self.fields["cell"].choices = [("", "Select cell")] + self.get_cell_choices(
                    instance.ward
                )

        # Ward → Cell dynamic filtering
        if data and "ward" in data:
            ward_value = data.get("ward")
            self.fields["cell"].choices = [("", "Select cell")] + self.get_cell_choices(
                ward_value
            )

    def get_ward_choices(self, division):
        """Return filtered ward choices based on division."""
        if division == "South_Division":
            return [
                ("Kakoba Ward", "Kakoba Ward"),
                ("Nyamityobora Ward", "Nyamityobora Ward"),
                ("Katete Ward", "Katete Ward"),
                ("Ruti Ward", "Ruti Ward"),
                ("Bugashe Ward", "Bugashe Ward"),
                ("Katojo Ward", "Katojo Ward"),
            ]
        if division == "North_Division":
            return [
                ("Rwenjeru Ward", "Rwenjeru Ward"),
                ("Nyabuhama Ward", "Nyabuhama Ward"),
                ("Biharwe East Ward", "Biharwe East Ward"),
                ("Biharwe West Ward", "Biharwe West Ward"),
                ("Kishasha Ward", "Kishasha Ward"),
                ("Kamukuzi Ward", "Kamukuzi Ward"),
                ("Ruharo Ward", "Ruharo Ward"),
                ("Kakiika Ward", "Kakiika Ward"),
                ("Rwemigina Ward", "Rwemigina Ward"),
            ]
        return []

    def get_cell_choices(self, ward):
        """Return filtered cell choices based on ward."""
        cell_dict = {
            # South Division wards
            "Kakoba Ward": [
                ("Kakoba Central", "Kakoba Central"),
                ("Kakoba Quarters", "Kakoba Quarters"),
                ("Kihindi", "Kihindi"),
                ("Kisenyi A", "Kisenyi A"),
                ("Kishwahili", "Kishwahili"),
                ("Kyapotani", "Kyapotani"),
                ("Lugazi", "Lugazi"),
                ("N.T.C", "N.T.C"),
                ("Nyakaizi", "Nyakaizi"),
                ("Police/Prisons", "Police/Prisons"),
                ("Rwentondo", "Rwentondo"),
                ("Mandela", "Mandela"),
            ],
            "Nyamityobora Ward": [
                ("Agip", "Agip"),
                ("Central", "Central"),
                ("Kabateraine", "Kabateraine"),
                ("Kilembe", "Kilembe"),
                ("Lower", "Lower"),
                ("Lubiri", "Lubiri"),
                ("Market", "Market"),
                ("Muti", "Muti"),
                ("Survey", "Survey"),
                ("Upper", "Upper"),
            ],
            "Katete Ward": [
                ("Bihunya", "Bihunya"),
                ("Karugangama", "Karugangama"),
                ("Katete Central", "Katete Central"),
                ("Kitebero", "Kitebero"),
                ("Nsikye", "Nsikye"),
                ("Nyamitanga", "Nyamitanga"),
                ("Rwemirinzi", "Rwemirinzi"),
                ("Rwizi", "Rwizi"),
            ],
            "Ruti Ward": [
                ("Kafunda", "Kafunda"),
                ("Kateera", "Kateera"),
                ("Kirehe", "Kirehe"),
                ("Market", "Market"),
                ("Nsikye", "Nsikye"),
                ("Nyamitanga", "Nyamitanga"),
                ("Rwizi", "Rwizi"),
                ("Tankhill", "Tankhill"),
            ],
            "Bugashe Ward": [
                ("Bugashe", "Bugashe"),
                ("Kanyamurimi", "Kanyamurimi"),
                ("Kibaya I", "Kibaya I"),
                ("Kibaya II", "Kibaya II"),
                ("Kibona", "Kibona"),
                ("Nyakahanga", "Nyakahanga"),
                ("Rutooma", "Rutooma"),
            ],
            "Katojo Ward": [
                ("Karugyembe", "Karugyembe"),
                ("Kitojo", "Kitojo"),
                ("Kibingo", "Kibingo"),
                ("Kitagata", "Kitagata"),
                ("Kitooma", "Kitooma"),
                ("Ngaara", "Ngaara"),
                ("Nyakashambya", "Nyakashambya"),
                ("Rwariire I", "Rwariire I"),
                ("Rwariire II", "Rwariire II"),
                ("Rwemigina", "Rwemigina"),
                ("Rwentondo", "Rwentondo"),
            ],

            # North Division wards
            "Rwenjeru Ward": [
                ("Rwendama", "Rwendama"),
                ("Rwenjeru South", "Rwenjeru South"),
                ("Kamatarisi", "Kamatarisi"),
                ("Kabucebebe", "Kabucebebe"),
                ("Rwakaterere", "Rwakaterere"),
                ("Rwenjeru North", "Rwenjeru North"),
                ("Katengyeto", "Katengyeto"),
                ("Katerananga", "Katerananga"),
                ("Akaku/Rwenjeru Wd", "Akaku/Rwenjeru Wd"),
            ],
            "Nyabuhama Ward": [
                ("Ekigando", "Ekigando"),
                ("Nyaruhanga", "Nyaruhanga"),
                ("Katojo", "Katojo"),
                ("Rugarama", "Rugarama"),
                ("Kakukuru", "Kakukuru"),
                ("Rwebishekye", "Rwebishekye"),
            ],
            "Biharwe East Ward": [
                ("Kyanyarukondo 1", "Kyanyarukondo 1"),
                ("Rwemirabyo", "Rwemirabyo"),
                ("Rwenkanja", "Rwenkanja"),
                ("Kasharara", "Kasharara"),
            ],
            "Biharwe West Ward": [
                ("Biharwe East", "Biharwe East"),
                ("Biharwe Central 11", "Biharwe Central 11"),
                ("Kyanyarukondo 11", "Kyanyarukondo 11"),
                ("Ekihangire", "Ekihangire"),
                ("Mailo", "Mailo"),
                ("Biharwe West", "Biharwe West"),
                ("Biharwe Central 1", "Biharwe Central 1"),
                ("Kanyara", "Kanyara"),
            ],
            "Kishasha Ward": [
                ("Kyempitsi", "Kyempitsi"),
                ("Kinyaza", "Kinyaza"),
                ("Nyakanengo", "Nyakanengo"),
                ("Rwabukwire", "Rwabukwire"),
                ("Rwobuyenje North", "Rwobuyenje North"),
                ("Kibungo", "Kibungo"),
                ("Rwobuyenje West", "Rwobuyenje West"),
                ("Nyamabare", "Nyamabare"),
            ],
            "Kamukuzi Ward": [
                ("Biafra Cell", "Biafra Cell"),
                ("Boma Cell", "Boma Cell"),
                ("Kakiika Cell", "Kakiika Cell"),
                ("Kakyeka Cell", "Kakyeka Cell"),
                ("Kamukuzi Cell", "Kamukuzi Cell"),
                ("Kashanyarazi Cell", "Kashanyarazi Cell"),
                ("Medical Cell", "Medical Cell"),
                ("Ntare Cell", "Ntare Cell"),
                ("Rwebikoona Cell", "Rwebikoona Cell"),
            ],
            "Ruharo Ward": [
                ("Kiyanja Cell", "Kiyanja Cell"),
                ("Mbaguta Cell", "Mbaguta Cell"),
                ("Mbarara High School", "Mbarara High School"),
                ("Nkokonjeru Cell", "Nkokonjeru Cell"),
                ("Rwizi Cell", "Rwizi Cell"),
            ],
            "Kakiika Ward": [
                ("Makenke Cell", "Makenke Cell"),
                ("Nyakabungo Cell", "Nyakabungo Cell"),
                ("Nyakiziba Cell", "Nyakiziba Cell"),
                ("Butagatsi Cell", "Butagatsi Cell"),
                ("Kacence East Cell", "Kacence East Cell"),
                ("Kacence West Cell", "Kacence West Cell"),
                ("Rwobuyenje Cell", "Rwobuyenje Cell"),
            ],
            "Rwemigina Ward": [
                ("Rwemigina Central Cell", "Rwemigina Central Cell"),
                ("Kabingo Cell", "Kabingo Cell"),
                ("Rwebiihuro Cell", "Rwebiihuro Cell"),
                ("Buremba I Cell", "Buremba I Cell"),
                ("Buremba II Cell", "Buremba II Cell"),
                ("Kenkombe Cell", "Kenkombe Cell"),
            ],
        }
        return cell_dict.get(ward, [])


# ---------------------------------------
# Property Information Form
# ---------------------------------------
class PropertyInformationForm(forms.ModelForm):
    class Meta:
        model = PropertyInformation
        # Don't let user edit captured_by / timestamps in the form
        exclude = ("created_at", "updated_at", "captured_by")
        widgets = {
            "property_no": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "street": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "property_number_plate": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "development_type": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "fencing_gate_type": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "property_usage": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "road_reserve_minimum": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "coordinates": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "no_units_on_property": forms.NumberInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "no_users_occupants": forms.NumberInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "owner_name": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "owner_phone_no": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "owner_email": forms.EmailInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "property_location": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "latitude": forms.NumberInput(
                attrs={
                    "step": "any",
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
                }
            ),
            "longitude": forms.NumberInput(
                attrs={
                    "step": "any",
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
                }
            ),
            "verified": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 text-indigo-600 focus:ring-indigo-500 "
                    "border-gray-300 rounded"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
                    "rows": 3,
                }
            ),
        }


# ---------------------------------------
# Concern Form (Town Agent + Planner)
# ---------------------------------------
class ConcernForm(forms.ModelForm):
    """
    Town agents react to concerns:
      - add a comment (agent_notes)
      - choose APPROVE or DEFEAT (agent_decision)

    Planners / Administrators:
      - manage overall status (status)
      - add confirmation notes.
    """

    class Meta:
        model = Concern
        fields = ["status", "agent_decision", "agent_notes", "confirmation_notes"]
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "agent_decision": forms.Select(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                }
            ),
            "agent_notes": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
                    "rows": 3,
                    "placeholder": "Town Agent remarks about the concern/property...",
                }
            ),
            "confirmation_notes": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md "
                    "shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
                    "rows": 3,
                    "placeholder": "Planning / administrative notes, resolution details, etc.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        # user is passed in from the view: ConcernForm(..., user=request.user)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Default choices from model
        self.fields["status"].choices = Concern.STATUS_CHOICES
        self.fields["agent_decision"].choices = [("", "Select decision")] + list(
            Concern.AGENT_DECISION_CHOICES
        )

        # Default: everything editable (we'll lock based on role)
        self.profile = getattr(self.user, "profile", None) if self.user else None

        if not self.user or not self.profile:
            # If no user / profile, make form read-only
            self._make_readonly()
            return

        role = self.profile.role

        # Town Agent behaviour
        if role == "town_agent":
            # Town agent focuses on decision + comment only
            # Status will be updated in the view based on decision.
            self.fields["status"].disabled = True
            self.fields["confirmation_notes"].widget = forms.HiddenInput()
            self.fields["agent_decision"].required = True

            # If concern already handled, lock agent_decision as well
            if self.instance and self.instance.pk and self.instance.agent_decision:
                self.fields["agent_decision"].disabled = True

        # Planner / Administrator behaviour
        elif role in ("planner", "administrator"):
            # They manage status & confirmation notes
            # Agent decision is informative (can disable editing if you want)
            # Here we allow them to see it but not change it:
            self.fields["agent_decision"].disabled = True

        # Other roles → read-only
        else:
            self._make_readonly()

    def _make_readonly(self):
        """Lock all fields for non-authorized users."""
        for field in self.fields.values():
            field.disabled = True
            field.widget.attrs["readonly"] = True

    def clean(self):
        cleaned = super().clean()

        if self.profile and self.profile.role == "town_agent":
            decision = cleaned.get("agent_decision")
            if not decision:
                self.add_error("agent_decision", "You must choose approve or defeat.")
        return cleaned
