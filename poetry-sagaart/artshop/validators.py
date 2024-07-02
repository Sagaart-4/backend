from django.core.exceptions import ValidationError
from django.utils import timezone

MIN_YEAR = 1800


def year_validator(year_of_creation):
    if year_of_creation > (timezone.now().year):
        raise ValidationError("Произведения из будущего нельзя добавлять")
    elif year_of_creation < MIN_YEAR:
        raise ValidationError(
            f"Продажа произведений созданных ранее {MIN_YEAR} года недоступна"
            "Обратитесь к администратору сайта для разъеснения."
        )
    return year_of_creation
