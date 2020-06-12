az account list -o tsv | grep 531ff96d | awk '{print$6}'
# touch address_prefixes.json
# for i in `az account list -o tsv | grep 531ff96d | awk '{print$6}'`; \
# do az account set --subscription $i; \
# az network vnet list --query '[].{Name:name, Location:location, ResourceGroup:resourceGroup, Network:addressSpace.addressPrefixes}' -o json >$i.json; \
# jq '.[] += {"ID": "'$i'"}' $i.json > $i.tmp && mv $i.tmp $i.json -f; \
# echo $(jq -s '[.[][]]' $i.json address_prefixes.json) >| address_prefixes.json; \
# rm $i.json; \
# done