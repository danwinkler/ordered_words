import os
import sys
import json

from tqdm import *

# Django stuff
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", "orderedwords.settings" )
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from analysis.analyze import (
    Korean,
    Japanese
)

from learn.models import (
    Language,
    Sentence,
    POS,
    Morph
)

def import_file( name, lang ):
    # Load data
    path = os.path.join( "analysis", "texts", name )
    with open( os.path.join( path, "sentences.json" ), encoding="utf8" ) as f:
        sentences = json.loads( f.read() )

    with open( os.path.join( path, "morph_map.json" ), encoding="utf8" ) as f:
        morph_map = json.loads( f.read() )

    # Prepare DB
    language, created = Language.objects.get_or_create(
        code = lang.code,
        name = lang.name
    )
    Sentence.objects.filter( filename=name ).delete()

    # Bulk create morphs
    print( name + " GET OR CREATE MORPHS" )
    p_map = {}
    ms = []
    for key, value in tqdm(morph_map.items()):
        morph, pos = key.split( lang.morph_delimiter )
        if pos not in p_map:
            p, created = POS.objects.get_or_create( name=pos, language=language )
            p_map[pos] = p
        m, created = Morph.objects.get_or_create( text=morph, pos=p_map[pos], language=language )
        ms.append( m )

    #Bulk create sentences
    print( name + " BULK CREATE SENTENCES" )
    s_list = [
        Sentence( filename=name, text=sentence, language=language ) for sentence in sentences
    ]

    Sentence.objects.bulk_create( s_list )

    #Add sentences to morphs
    print( name + " MAP MORPHS TO SENTENCES" )
    ss = Sentence.objects.filter( filename=name ).all().prefetch_related( 'language' )

    m_map = {}
    s_map = {}

    print( name + "   BUILD M MAP" )
    for key, value in tqdm(morph_map.items()):
        morph, pos = key.split( lang.morph_delimiter )
        for m in ms:
            if m.text == morph and m.pos.name == pos and m.language == language:
                m_map[morph] = m
                break

    print( name + "   BUILD S MAP" )
    for sentence in tqdm(sentences):
        for s in ss:
            if s.filename == name and s.text == sentence and s.language == language:
                s_map[sentence] = s

    print( name + "   ASSOCIATE" )
    unique_pairs = {}
    ThroughModel = Morph.sentences.through
    t_list = []
    for key, value in tqdm(morph_map.items()):
        morph, pos = key.split( lang.morph_delimiter )
        for sentence in value:
            morph_id = m_map[morph].pk
            sentence_id = s_map[sentences[sentence]].pk
            tup = (morph_id, sentence_id)
            if tup not in unique_pairs:
                t_list.append( ThroughModel( morph_id=morph_id, sentence_id=sentence_id ) )
                unique_pairs[tup] = 1


    print( name + "   SAVE" )
    ThroughModel.objects.bulk_create( t_list )

def set_pos( name, label, desc, lang ):
    language, created = Language.objects.get_or_create(
        code = lang.code,
        name = lang.name
    )
    POS.objects.update_or_create(
        name=name,
        language=language,
        defaults={
            'label': label,
            'desc': desc
        }
    )

##    ##  #######  ########  ########    ###    ##    ##
##   ##  ##     ## ##     ## ##         ## ##   ###   ##
##  ##   ##     ## ##     ## ##        ##   ##  ####  ##
#####    ##     ## ########  ######   ##     ## ## ## ##
##  ##   ##     ## ##   ##   ##       ######### ##  ####
##   ##  ##     ## ##    ##  ##       ##     ## ##   ###
##    ##  #######  ##     ## ######## ##     ## ##    ##

set_pos( "NNG", "Plain Noun", "", Korean() )
set_pos( "NNP", "Proper Noun", "", Korean() )

'''
import_file( "hp1_ko", Korean() )
import_file( "hp2_ko", Korean() )
import_file( "hp3_ko", Korean() )
import_file( "hp4_ko", Korean() )
import_file( "hp5_ko", Korean() )
import_file( "hp6_ko", Korean() )
import_file( "hp7_ko", Korean() )
'''
      ##    ###    ########     ###    ##    ## ########  ######  ########
      ##   ## ##   ##     ##   ## ##   ###   ## ##       ##    ## ##
      ##  ##   ##  ##     ##  ##   ##  ####  ## ##       ##       ##
      ## ##     ## ########  ##     ## ## ## ## ######    ######  ######
##    ## ######### ##        ######### ##  #### ##             ## ##
##    ## ##     ## ##        ##     ## ##   ### ##       ##    ## ##
 ######  ##     ## ##        ##     ## ##    ## ########  ######  ########

import_file( "hp1_jp", Japanese() )
