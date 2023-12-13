@echo off
echo 1. blanksorter.py
echo 2. redlinesorter.py
echo Please select a script to run (1-2):

CHOICE /C 12 /N /M ">"
IF ERRORLEVEL 2 goto selection2
IF ERRORLEVEL 1 goto selection1

:selection1
echo You selected blanksorter.py
python blanksorter.py
goto end

:selection2
echo You selected redlinesorter.py
python redlinesorter.py
goto end

:end
