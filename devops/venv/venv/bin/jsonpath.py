#!/home/yogesh/PycharmProjects/devops/venv/venv/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'jsonpath-rw==1.3.0','console_scripts','jsonpath.py'
__requires__ = 'jsonpath-rw==1.3.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('jsonpath-rw==1.3.0', 'console_scripts', 'jsonpath.py')()
    )
