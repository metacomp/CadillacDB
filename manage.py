#!/home/metacomp/src/ianb-virtualenv-1f9dfb2437f1/py2.7/bin/python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itp_clc.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
