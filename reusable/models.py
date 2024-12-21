import logging
from decimal import Decimal
from typing import Optional, Any

from django.db import models

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    """
    Abstract base model with indexed `created_at` and `updated_at` fields for tracking object timestamps and improving query performance.
    """

    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True, db_index=True
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.id}"

    class Meta:
        abstract = True


class AmountField(models.DecimalField):
    """
    Custom DecimalField for representing precise amounts, with high precision and predefined limits.

    Attributes:
        INTEGER_PLACES (int): Number of digits before the decimal point.
        DECIMAL_PLACES (int): Number of digits after the decimal point.
        DECIMAL_PLACES_FOR_USER (int): User-facing precision for amounts.
        MAX_DIGITS (int): Total maximum digits allowed.
        MAX_VALUE (Decimal): Maximum allowable value.
        MIN_VALUE (Decimal): Minimum allowable value.
    """

    INTEGER_PLACES: int = 20
    DECIMAL_PLACES: int = 18
    DECIMAL_PLACES_FOR_USER: int = 6

    MAX_DIGITS: int = INTEGER_PLACES + DECIMAL_PLACES
    MAX_VALUE: Decimal = Decimal("99999999999999999999.999999999999999999")
    MIN_VALUE: Decimal = Decimal("-99999999999999999999.999999999999999999")

    def __init__(
        self,
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        max_digits: int = MAX_DIGITS,
        decimal_places: int = DECIMAL_PLACES,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the AmountField with default precision and constraints.

        Args:
            verbose_name (Optional[str]): The human-readable name for the field.
            name (Optional[str]): The field name within the model.
            max_digits (int): Maximum number of digits for the field.
            decimal_places (int): Number of decimal places for the field.
            **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(
            verbose_name=verbose_name,
            name=name,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **kwargs,
        )


class PercentageField(models.DecimalField):
    """
    Custom DecimalField for representing percentages, with limited precision and predefined constraints.

    Attributes:
        INTEGER_PLACES (int): Number of digits before the decimal point.
        DECIMAL_PLACES (int): Number of digits after the decimal point.
        MAX_DIGITS (int): Total maximum digits allowed.
        MAX_VALUE (Decimal): Maximum allowable value.
        MIN_VALUE (Decimal): Minimum allowable value.
    """

    INTEGER_PLACES: int = 2
    DECIMAL_PLACES: int = 2

    MAX_DIGITS: int = INTEGER_PLACES + DECIMAL_PLACES
    MAX_VALUE: Decimal = Decimal("99.99")
    MIN_VALUE: Decimal = Decimal("-99.99")

    def __init__(
        self,
        verbose_name: Optional[str] = None,
        name: Optional[str] = None,
        max_digits: int = MAX_DIGITS,
        decimal_places: int = DECIMAL_PLACES,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the PercentageField with default precision and constraints.

        Args:
            verbose_name (Optional[str]): The human-readable name for the field.
            name (Optional[str]): The field name within the model.
            max_digits (int): Maximum number of digits for the field.
            decimal_places (int): Number of decimal places for the field.
            **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(
            verbose_name=verbose_name,
            name=name,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **kwargs,
        )
