mkdir -p ./downloaded
wget -i ./data_urls.txt -P ./downloaded 
bzip2 -d ./downloaded/*.bz2
gzip -d ./downloaded/*.gz