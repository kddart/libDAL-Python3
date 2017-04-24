import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages, setup

if not (sys.version_info > (3, 0)):
    # Python 3 code in this block
    sys.stderr.write("""
    This setup needs to be run with python3 not python!
    Please retry the command:
        sudo python3 %s

    """ % " ".join(sys.argv))
    sys.exit(1)

VERSION = "1.0.1"

overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "dalclient"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break


EXCLUDE_FROM_PACKAGES = ['dalclient.bin']

setup(
    name='Python3-DALClient',
    version=VERSION,
    url='https://www.kddart.org/',
    author='Diversity Arrays Technology',
    author_email='kdxplore@diversityarrays.com',
    description=('A Python3 Utility for connecting to KDDart database installations'
                 'through the Data Access Layer (DAL) REST API'),
    license='GPLv3',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: Alpha',
        'Environment :: Development Environment',
        'Framework :: DALClient',
        'Intended Audience :: Developers',
        'License :: GPLv3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)


if overlay_warning:
    sys.stderr.write("""
 +-+-+-+-+-+-+-+
 |W|A|R|N|I|N|G|
 +-+-+-+-+-+-+-+
You have installed Python2 DALClient over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed. You
should manually remove the
%(existing_path)s
directory and re-install Python2 DALCLient.
""" % {"existing_path": existing_path})
else:
    sys.stdout.write("""
  ___   _   _    ___ _ _         _
 |   \ /_\ | |  / __| (_)___ _ _| |_
 | |) / _ \| |_| (__| | / -_) ' \  _|
 |___/_/ \_\____\___|_|_\___|_||_\__|
 INSTALLED SUCCESSFULLY For Python 3!
    """)
