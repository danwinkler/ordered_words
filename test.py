import nltk

from konlpy.corpus import kobill
from konlpy.tag import Twitter; t = Twitter()

from konlpy.tag import Hannanum
hannanum = Hannanum()

from konlpy.tag import Kkma
kkma = Kkma()

files = kobill.fileids()

text = kobill.open('1809890.txt').read()

print( text[:15] )

tokens = kkma.morphs( text )

ko = nltk.Text( tokens, name='대한민국 국회 의안 제 1809890호' )

print( ko.findall( "<.*><가>" ) )
