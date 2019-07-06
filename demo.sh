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


for i in "${names[@]}"
do
    curl -X POST "http://localhost:3778/jobs?name=${i}"
done
