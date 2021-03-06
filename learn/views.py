from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Count
from django.db.models.functions import Length
from django.contrib.auth.decorators import user_passes_test

from learn import language

from .models import (
    Sentence,
    Morph,
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

        if 'pos' in self.request.GET:
            q = q.filter( pos__name__startswith=self.request.GET['pos'] )

        return q

class MorphDetailView( DetailView ):
    model = Morph

class SentenceListView( ListView ):
    model = Sentence
    paginate_by = 50

    def get_queryset( self ):
        q = Sentence.objects.all()

        if 'language' in self.request.GET:
            q = q.filter( language__code=self.request.GET['language'] )

        if 'file' in self.request.GET:
            q = q.filter( filename=self.request.GET['file'] )

        return q

class SentenceDetailView( DetailView ):
    model = Sentence
