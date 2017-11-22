num_lines=`cat $PWD/ddash/data/static-nodes.json | wc -l`
echo number of lines: "$num_lines"

read -p "enter enode: " enode

i=0

while IFS= read -r line 
do
    echo i equals "$i"
    echo num_lines minus two equals "$[num_lines-2]"

    if [[ $num_lines -gt 2 ]] && [[ $i -eq $[num_lines-2] ]]; then
        echo add comma
        echo "$line", >> $PWD/ddash/data/static-nodes2.json
    else
        echo "$line" >> $PWD/ddash/data/static-nodes2.json
    fi

    if [ $i = $[$num_lines-2] ]; then
        echo "$enode" >> $PWD/ddash/data/static-nodes2.json
    fi
    i=$[i+1]

done < "$PWD/ddash/data/static-nodes.json"

mv $PWD/ddash/data/static-nodes2.json $PWD/ddash/data/static-nodes.json

