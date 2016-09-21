#!/bin/bash
coverage run --source epanettools setup.py test
coverage html  --omit=epanettools/examples/simple/epanet2_test.py 

URL='./htmlcov/index.html'
[[ -x $BROWSER ]] && exec "$BROWSER" "$URL"
path=$(which xdg-open || which gnome-open) && exec "$path" "$URL"
echo "Can't find browser"
