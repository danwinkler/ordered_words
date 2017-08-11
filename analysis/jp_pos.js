var RakutenMA = require('../node_modules/rakutenma');
var fs = require('fs');

var model = JSON.parse( fs.readFileSync( "../node_modules/rakutenma/model_ja.json" ) );
rma = new RakutenMA( model, 1024, 0.007812 );  // Specify hyperparameter for SCW (for demonstration purpose)
rma.featset = RakutenMA.default_featset_ja;

rma.hash_func = RakutenMA.create_hash_func(15);

var sentences = JSON.parse( fs.readFileSync( "jp_pos_temp.json" ) );
var pos_tags = {};

for( var i in sentences )
{
    process.stdout.write("\r " + (i / sentences.length) );
    pos_tags[sentences[i]] = rma.tokenize( sentences[i] );
}

fs.writeFile( "jp_pos_temp_out.json", JSON.stringify( pos_tags ) );
