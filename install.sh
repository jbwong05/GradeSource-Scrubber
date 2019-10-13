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

pip3 install -r requirements.txt

echo '#!/usr/bin/python3' > graderetriever
cat ./GradeRetriever.py >> graderetriever

chmod +x ./graderetriever

cp ./graderetriever /usr/local/bin/
