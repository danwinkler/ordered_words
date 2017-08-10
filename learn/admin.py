from django.contrib import admin

from .models import (
    Language,
    POS,
    Sentence,
    Morph
)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(POS)
class POSAdmin(admin.ModelAdmin):
    pass

@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Morph)
class MorphAdmin(admin.ModelAdmin):
    list_display = ('text', 'sentence_count')

    def sentence_count( self, obj ):
        return obj.sentences.count()

    sentence_count.admin_order_field = 'sentences__count'
