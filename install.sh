#!/bin/bash

# Checks for sudo
echo -n "Checking permissions... "
if [[ $(id -u) -ne 0 ]]
then
    echo "FAIL! Rerun with sudo"
    exit 0
else
    echo "PASS!"
fi

echo '#!/usr/bin/python3' > graderetriever
cat ./GradeRetriever.py >> graderetriever

chmod +x ./graderetriever

cp ./graderetriever /usr/local/bin/
