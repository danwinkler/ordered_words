import os
import json

from konlpy.tag import Kkma
from konlpy.utils import pprint

from jnltk.tokenize import SimpleRuleSntenceTokenizer
from jptokenizer import JPSimpleTokenizer

class Korean:
    def __init__( self ):
        self.kkma = Kkma()

    def sentences( self, text ):
        return self.kkma.sentences( text )

    def morphs( self, text ):
        return self.kkma.morphs( text )

class Japanese:
    def __init__( self ):
        self.tokenizer = SimpleRuleSntenceTokenizer()
        self.morph_tokenizer = JPSimpleTokenizer()

    def sentences( self, text ):
        return self.tokenizer.tokenize( text )

    def morphs( self, text ):
        return self.morph_tokenizer.tokenize( text )

def analyse( filename, nla ):
    if not os.path.exists( filename ):
        raise Exception( "Text file " + filename + " doesnt exist." )

    folder = filename.rsplit('.', 1)[0]
    if not os.path.exists( folder ):
        os.makedirs( folder )

    sentence_file = os.path.join( folder, "sentences.json" )
    if not os.path.exists( sentence_file ):
        with open( filename, encoding="utf8" ) as f:
            text = f.read()

        sentences = nla.sentences( text )

        with open( sentence_file, 'w', encoding="utf8" ) as f:
            f.write( json.dumps( sentences, ensure_ascii=False ) )
    else:
        with open( sentence_file, encoding="utf8" ) as f:
            sentences = json.loads( f.read() )

    morph_map_file = os.path.join( folder, "morph_map.json" )
    if not os.path.exists( morph_map_file ):
        morph_map = {}

        for i in range( len( sentences ) ):
            if i % 10 == 0:
                print( "Morph map ", i / len( sentences ) )
            sentence = sentences[i]
            morphs = nla.morphs( sentence )
            for morph in morphs:
                if morph not in morph_map:
                    morph_map[morph] = []
                morph_map[morph].append( i )

        with open( morph_map_file, 'w', encoding="utf8" ) as f:
            f.write( json.dumps( morph_map, ensure_ascii=False ) )

    else:
        with open( morph_map_file, encoding="utf8" ) as f:
            morph_map = json.loads( f.read() )

    morph_freq_file = os.path.join( folder, "morph_freq.txt" )
    if not os.path.exists( morph_freq_file ):
        morphs = sorted( morph_map.items(), key=lambda x: len(x[1]), reverse=True )
        with open( morph_freq_file, 'w', encoding="utf8" ) as f:
            for morph in morphs:
                f.write( morph[0] + " " + str(len(morph[1])) + "\n" )

analyse( "texts/hp1_ko.txt", Korean() )
analyse( "texts/hp1_jp.txt", Japanese() )
