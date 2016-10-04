deactivate
VIRTUALENVWRAPPER_PYTHON=python3
rmvirtualenv epanettools
mkvirtualenv epanettools --no-site-packages
workon epanettools
pip install -r requirements.txt
