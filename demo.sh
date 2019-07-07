# demo.sh
#
# This script sets up some data for the front-end to display.
# 
# For this script to function properly, start up the service 
# containers first.

set -e

echo "
===============================================================================

    Loading sample data
    Depending on your network condition, this may take several minutes.

    Beta note:
        The script ends immediately, but the containers are still processing
        the script's requests. In a future version, the script won't terminate
        until all requests are successful, or one of the requests failed.

===============================================================================
"

# install brew if not installed | update brew otherwise
which -s brew
if [[ $? != 0 ]] ; then
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    brew update
fi

brew install jq


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
        fi
        if [ "${status}" == '"Failed to complete"' ]; then
            printf "An error has occured in processing %-25b\n" "${name_arr[@]}"
            exit 1
        fi
    done
done

echo "All processing finished. Happy searching!"