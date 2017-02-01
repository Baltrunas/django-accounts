from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from .models import PromoCode


class PromoCodeTranslationOptions(TranslationOptions):
	fields = ['name', 'description']

translator.register(PromoCode, PromoCodeTranslationOptions)
