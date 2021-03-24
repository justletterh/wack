#!/bin/bash
if ! [[ -f "db/colors.db" ]];then
cd ./db
/bin/bash ./gen.sh
cd ./..
fi
npm start