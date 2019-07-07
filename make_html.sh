#!/bin/sh

pandoc -f markdown -t rst -o swagccg/docs/source/README.rst README.md
swagccg/docs/make html
echo "MAKE SCRIPT FINISHED"
