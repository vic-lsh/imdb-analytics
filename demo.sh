# demo.sh
#
# This script sets up some data for the front-end to display.
# 
# For this script to function properly, start up the service 
# containers first.

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
    brew update
fi

brew install jq

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

declare -a id_arr=()

for i in "${names[@]}"
do
    resp=$(curl -s -X POST "http://localhost:3778/jobs?name=${i}")
    id=$(echo ${resp} | jq '.id')
    name=$(echo ${resp} | jq '.name')
    printf 'Start processing TV show %-25b id: %-10d\n' "${name}" ${id}
    id_arr+=($id)
done

declare -p id_arr
