# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .choices import (
    DIVISION_CHOICES,
    WARD_CHOICES,
    CELL_CHOICES,
    WARD_TO_DIVISION,
)


class Profile(models.Model):
    """
    Extension of Django's built-in User with role and location.
    - division: single division (South / North)
    - ward: single ward
    - cell: single cell
    """

    ROLE_TOWN_AGENT = "town_agent"
    ROLE_PLANNER = "planner"
    ROLE_ADMINISTRATOR = "administrator"

    ROLE_CHOICES = [
        (ROLE_TOWN_AGENT, "Town Agent"),
        (ROLE_PLANNER, "Planner"),
        (ROLE_ADMINISTRATOR, "Administrator"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_TOWN_AGENT,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    # Location fields – all single-select with fixed choices
    division = models.CharField(
        max_length=50,
        choices=DIVISION_CHOICES,
        blank=True,
        null=True,
        help_text="Division / area of assignment",
    )

    ward = models.CharField(
        max_length=100,
        choices=WARD_CHOICES,
        blank=True,
        null=True,
        help_text="Ward of assignment",
    )

    cell = models.CharField(
        max_length=100,
        choices=CELL_CHOICES,
        blank=True,
        null=True,
        help_text="Cell of assignment",
    )

    def clean(self):
        """
        Enforce:
        - selected ward must belong to selected division.

        NOTE: We do NOT strictly validate cell → ward here because
        some cell names (e.g. 'Market', 'Nsikye', 'Rwizi') appear
        under more than one ward in the data.
        """
        super().clean()

        if self.ward:
            expected_division = WARD_TO_DIVISION.get(self.ward)
            if expected_division and self.division and self.division != expected_division:
                raise ValidationError({
                    "ward": (
                        f"{self.ward} belongs to "
                        f"{expected_division.replace('_', ' ')}, "
                        f"but you selected {self.division.replace('_', ' ')}."
                    )
                })

    def __str__(self) -> str:
        return f"{self.user.get_username()} - {self.get_role_display()}"
