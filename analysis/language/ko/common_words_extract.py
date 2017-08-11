import re
import json

with open( "common_words.txt", encoding='utf8' ) as f:
    text = f.read()

lines = text.split( "\n" )[1:]

words = []

lsplit = re.compile( "\t" )
for line in lines:
    parts = [s.strip() for s in lsplit.split( line )]
    if len(parts) == 5:
        words.append( parts[3:])

with open( "common_words_standard.json", 'w', encoding='utf8' ) as f:
    f.write( json.dumps( words, ensure_ascii=False ) )
