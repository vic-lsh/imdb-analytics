# demo.sh
#
# This script sets up some data for the front-end to display.
# 
# For this script to function properly, start up the service 
# containers first.

arr_del () {
    del=$1
    arr=$2
    # printf "deleting %d\n" $del
    delete=($del)
    echo ${id_arr[@]/$delete}
}

set -e

echo "
===============================================================================

    Loading sample data
    Depending on your network condition, this may take several minutes.

===============================================================================
"

# install brew if not installed | update brew otherwise
which -s brew
if [[ $? != 0 ]] ; then
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    brew update > /dev/null
fi


# install jq
if brew ls --versions jq > /dev/null; then
    continue
else
    brew install jq
fi


# tv shows to query
declare -a names=("Game+of+Thrones" 
                  "How+I+met+Your+Mother" 
                  "Black+Mirror"
                  "Breaking+Bad"
                  "Friends"
                  "The+Simpsons"
                  "The+Office"
                  "Stranger+Things"
                  "Futurama"
                  "Big+Little+Lies")


# initiate queries
declare -a id_arr=()
declare -a name_arr=()

for i in "${names[@]}"
do
    resp=$(curl -s -X POST "http://localhost:3778/jobs?name=${i}")
    id=$(echo ${resp} | jq '.id')
    name=$(echo ${resp} | jq '.name')
    id_arr+=($id)
    name_arr+=("$name")
    printf 'Start processing TV show %-25b id: %-10d\n' "${name}" ${id}
done


# check if all queries are completed successfully
len=${#id_arr[@]}
while ((ctr < len))
do
    sleep 5s
    ctr=0
    for i in "${id_arr[@]}"
    do
        resp=$(curl -s -X GET "http://localhost:3778/jobs/${i}")
        status=$(echo ${resp} | jq '.status')
        if [ "${status}" = '"Completed successfully"' ]; then
            ctr=`expr $ctr + 1`

            del_id=($i)
            echo ${id_arr[@]/$del_id}
            id_arr=( "${id_arr[@]/$del_id}" )
            echo ${#id_arr[@]}

            del_name=($i)
            echo ${name_arr[@]/$del_name}
            name_arr=( "${name_arr[@]/$del_name}" )


        fi
        if [ "${status}" == '"Failed to complete"' ]; then
            printf "An error has occured in processing %-25b\n" "${name_arr[@]}"
            exit 1
        fi
    done
done

echo "
All processes finished. 
You may now try to search for one of the processed TV shows listed above.
Happy searching!
"