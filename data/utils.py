from django.utils import translation
import locale


def sort_by_uk(value):
    if translation.get_language() == 'uk':
        return sorted(value, key=lambda x: locale.strxfrm(x.title))
    else:
        return value
