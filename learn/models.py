from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    code = models.CharField( max_length=10 )
    name = models.TextField()

    def __str__( self ):
        return self.name

class Sentence(models.Model):
    text = models.TextField()
    language = models.ForeignKey( Language )
    filename = models.CharField( max_length=40 )
    translations = models.ManyToManyField( "Sentence" )

    def __str__( self ):
        return self.text

class POS(models.Model):
    name = models.CharField( max_length=10 )
    label = models.CharField( max_length=40, blank=True )
    desc = models.TextField( blank=True )
    language = models.ForeignKey( Language )

    def __str__( self ):
        return self.name

class CommonWord(models.Model):
    text = models.TextField()
    desc = models.TextField()
    language = models.ForeignKey( Language )

    def __str__( self ):
        return self.text

class Morph(models.Model):
    unique_text = models.TextField() # Bass (Fish), Bass (Instrument)
    text = models.TextField() # Bass
    pos = models.ForeignKey( POS )
    sentences = models.ManyToManyField( Sentence )
    language = models.ForeignKey( Language )
    common = models.ForeignKey( CommonWord, null=True )

    def __str__( self ):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField( User )
    morphs = models.ManyToManyField( Morph )
    language = models.ForeignKey( Language )
