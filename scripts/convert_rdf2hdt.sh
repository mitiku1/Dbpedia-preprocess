mkdir -p dbpedia-hdt
for filename in ./downloaded/*.nt;
do
    echo "Converting '$filename' to hdt";
    fname="$(basename -s .nt $filename)"
    
    rdf2hdt $filename "dbpedia-hdt/$fname.hdt"
done;



for filename in ./downloaded/*.ttl;
do
    echo "Converting '$filename' to hdt";
    fname="$(basename -s .ttl $filename)"
    
    rdf2hdt $filename "dbpedia-hdt/$fname.hdt"
done;