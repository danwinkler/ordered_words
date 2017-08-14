import os
import json

from tqdm import *

from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.utils import pprint

from jnltk.tokenize import SimpleRuleSntenceTokenizer

try:
    from .jptokenizer import JPSimpleTokenizer
except:
    from jptokenizer import JPSimpleTokenizer

from Naked.toolshed.shell import muterun_js, execute_js

class Korean:
    morph_delimiter = "_|_"
    code = 'ko'
    name = 'Korean'

    def __init__( self ):
        self.kkma = Kkma()
        self.hannanum = Hannanum()

    def sentences( self, text ):
        return self.kkma.sentences( text )

    def morphs( self, text ):
        return self.kkma.morphs( text )

    def pos( self, text ):
        return self.kkma.pos( text )

class Japanese:
    morph_delimiter = "_|_"
    code = 'jp'
    name = 'Japanese'

    def __init__( self ):
        self.tokenizer = SimpleRuleSntenceTokenizer()
        self.morph_tokenizer = JPSimpleTokenizer()

    def sentences( self, text ):
        return self.tokenizer.tokenize( text )

    def morphs( self, text ):
        return self.morph_tokenizer.tokenize( text )

    def batch_pos( self, sentences ):
        temp_file = "jp_pos_temp.json"
        with open( temp_file, 'w', encoding="utf8" ) as f:
            f.write( json.dumps( sentences, ensure_ascii=False ) )
        execute_js( "jp_pos.js" )
        with open( "jp_pos_temp_out.json", encoding="utf8" ) as f:
            ret = json.loads( f.read() )
        os.remove( temp_file )
        os.remove( "jp_pos_temp_out.json" )
        return ret

def analyse( filename, nla ):
    print( "analysing " + filename )
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

        print( "MORPH MAP" )
        if hasattr( nla, "batch_pos" ):
            sentence_pos_map = nla.batch_pos( sentences )
            for sentence, morphs in sentence_pos_map.items():
                i = sentences.index( sentence )
                for morph in morphs:
                    morph_t = nla.morph_delimiter.join( morph )
                    if morph_t not in morph_map:
                        morph_map[morph_t] = []
                    morph_map[morph_t].append( i )
        else:
            for i in tqdm( range( len( sentences ) ) ):
                sentence = sentences[i]
                morphs = nla.pos( sentence )
                for morph in morphs:
                    morph_t = nla.morph_delimiter.join( morph )
                    if morph_t not in morph_map:
                        morph_map[morph_t] = []
                    morph_map[morph_t].append( i )

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

if __name__ == "__main__":
    #We have our own init_jvm function so that we can start the jvm with more memory
    from konlpy_jpype_hack import init_jvm
    init_jvm()

    analyse( "texts/basic_ko.txt", Korean() )
    analyse( "texts/hp1_ko.txt", Korean() )
    analyse( "texts/hp2_ko.txt", Korean() )
    analyse( "texts/hp3_ko.txt", Korean() )
    analyse( "texts/hp4_ko.txt", Korean() )
    analyse( "texts/hp5_ko.txt", Korean() )
    analyse( "texts/hp6_ko.txt", Korean() )
    analyse( "texts/hp7_ko.txt", Korean() )
    analyse( "texts/hp1_jp.txt", Japanese() )
    analyse( "texts/jp_test.txt", Japanese() )
