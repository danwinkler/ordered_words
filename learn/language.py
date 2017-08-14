import os

from tqdm import *

#Korean
from konlpy.tag import Kkma

#Japanese
from rakutenma import RakutenMA

from .models import (
    Language,
    Sentence,
    POS,
    Morph
)

class LanguageMod:
    pass

class Korean(LanguageMod):
    code = "ko"
    kkma = Kkma()

    def sentences( text ):
        return Korean.kkma.sentences( text )

    def pos( sentence ):
        return Korean.kkma.pos( sentence )

class Japanese(LanguageMod):
    code = "ja"
    rma = None

    def sentences( text ):
        pass

    def pos( sentence ):
        if not Japanese.rma:
            Japanese.rma = RakutenMA( phi=1024, c=0.007812 )
            Japanese.rma.load( "node_modules/rakutenma/model_ja.json" )
        return Japanese.rma.tokenize( sentence )

language_mods = {
    "ja": Japanese,
    "ko": Korean
}

def get_mod( code ):
    return language_mods[code]

##     ## ########  ########     ###    ######## ########    ########     ###    ########    ###
##     ## ##     ## ##     ##   ## ##      ##    ##          ##     ##   ## ##      ##      ## ##
##     ## ##     ## ##     ##  ##   ##     ##    ##          ##     ##  ##   ##     ##     ##   ##
##     ## ########  ##     ## ##     ##    ##    ######      ##     ## ##     ##    ##    ##     ##
##     ## ##        ##     ## #########    ##    ##          ##     ## #########    ##    #########
##     ## ##        ##     ## ##     ##    ##    ##          ##     ## ##     ##    ##    ##     ##
 #######  ##        ########  ##     ##    ##    ########    ########  ##     ##    ##    ##     ##

def make_language( name, code ):
    o, c = Language.objects.get_or_create(
        name=name,
        code=code
    )

    return o

def make_sentence( text, language, mod ):
    pos = mod.pos( text )
    s, c = Sentence.objects.get_or_create(
        text=text,
        language=language
    )

    for t in pos:
        p, c = POS.objects.get_or_create(
            name=t[1],
            language=language
        )
        m, c = Morph.objects.get_or_create(
            text=t[0],
            language=language,
            pos=p
        )
        m.sentences.add( s )

def update_default_sentences( language ):
    default_sentence_file = os.path.join( "defaults", language.code + ".txt" )

    if not os.path.exists( default_sentence_file ):
        return

    with open( default_sentence_file, encoding="utf8" ) as f:
        text = f.read()

    mod = get_mod( language.code )

    #Defaults are always one sentence per line
    sentences = [s.strip() for s in text.split( "\n" )]

    #Filter zero length sentences
    sentences = filter( lambda s: len(s) > 0, sentences )

    for sentence in tqdm( sentences ):
        make_sentence( sentence, language, mod )

def update_data():
    make_language( "Korean", "ko" )
    make_language( "Japanese", "ja" )
    make_language( "English", "en" )
    make_language( "Spanish", "es" )

    for language in Language.objects.all():
        update_default_sentences( language )
