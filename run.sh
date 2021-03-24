#!/bin/sh
if ! [[ -f "db/colors.db" ]];then
cd ./db
/bin/sh ./gen
cd ./..
fi