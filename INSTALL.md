Do all the things below and stuff might work.  Figuring out how to hook
things up physically may require more poking around.

###
# RPi.GPIO
###

Check for latest version here: https://pypi.python.org/pypi/RPi.GPIO/

You can read the RPi docs to be sure, but installation probably look like:

    wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.9.tar.gz
    tar zxf RPi.GPIO-*.tar.gz
    cd RPi.GPIO-*
    sudo python setup.py install
    cd ..


###
# Crontab
###

Edit crontab and make sure it is using the correct path

    sudo cp crontab /etc/cron.d/access


###
# Running tests
###

If you feel so inclined (no raspberry pi required).

    pip install -r requirements.txt
    pip install -r dev_requirements.txt
    python tests.py
