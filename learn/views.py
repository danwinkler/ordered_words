from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Count
from django.db.models.functions import Length

from .models import (
    Sentence,
    Morph,
    CommonWord
)

def index( request ):
    pass

class MorphListView( ListView ):
    model = Morph
    paginate_by = 20
    def get_queryset( self ):
        q = Morph.objects\
            .annotate( text_len=Length( 'text' ) )\
            .filter( text_len__gt=1 )\
            .annotate( sentence_count=Count( 'sentences' ) )\
            .order_by( '-sentence_count' )

        if 'language' in self.request.GET:
            q = q.filter( language__code=self.request.GET['language'] )

        return q

class MorphDetailView( DetailView ):
    model = Morph

class SentenceDetailView( DetailView ):
    model = Sentence

    def get_context_data( self, **kwargs ):
        context = super().get_context_data( **kwargs )
        common = CommonWord.objects.filter( language=context['sentence'].language ).values_list( 'text', flat=True )
        context['good_words'] = context['sentence'].morph_set.filter( text__in=common )
        return context
