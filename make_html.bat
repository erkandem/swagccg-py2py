@ECHO OFF
pandoc -f markdown -t rst -o swagccg\docs\source\README.rst README.md
CALL swagccg\docs\make html
ECHO MAKE SCRIPT FINISHED