@echo off
if not exist db\colors.db (
    cd db
    gen&&cd ..
)
npm i>NUL
npm start