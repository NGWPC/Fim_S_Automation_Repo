#!/bin/bash

chmod +x /home/jyoti.mikkilineni/pw/automation/scripts/tests/utils/remove_file.sh
FILE=$1
echo $FILE
sudo rm -rf "$FILE"
echo "Deleted file"