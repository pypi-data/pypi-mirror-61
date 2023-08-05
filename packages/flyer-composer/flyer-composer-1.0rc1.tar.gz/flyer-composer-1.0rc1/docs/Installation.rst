
Download & Installation
=========================

Instructions for Windows Users
-----------------------------------

.. note:: Installation requires poppler and python-poppler-qt5, both of
   which are hardly available for Windows. Thus instructions for windows are
   incomplete.

1. |flyer-composer| requires Python 3. If you don't have Python 3
   installed already, download and install Python 3.7 (or a newer version)
   from https://python.org/download/

   During installation, make sure to check "Include into PATH".

2. If you already have Python installed, please check that your Python
   directory (normally :file:`C:\\Python37` for Python 3.7) and the Python
   Scripts directory (normally :file:`C:\\Python37\\Scripts`) are in the system
   path. If not, just add them in :menuselection:`My Computer --> Properties
   --> Advanced --> Environment Variables` to the :envvar:`Path` system
   variable.

3. Install |flyer-composer| and all requirements by running ::

     pip install flyer-composer

   Then run the console command ``flyer-composer --help`` to get detailed
   help.

   If the command ``pip`` is unknown to you system, please refer to the
   `pip homepage <https://pip.pypa.io/en/stable/installing/>`_ for help.


Instructions for GNU/Linux and other Operating Systems
--------------------------------------------------------

Most current GNU/Linux distributions provide packages for |flyer-composer|
and |flyer-composer-gui|.
Simply search your distribution's software catalog.

Also many vendors provide Python, and some even provide |flyer-composer|
and |flyer-composer-gui|.
Please check your vendor's software repository.

If your distribution or vendor does not provide a current version of
|flyer-composer| please read on.

If your vendor does not provide :command:`python3`
please download Python 3.7 from https://www.python.org/download/ and
follow the installation instructions there.

If you distribution or vendor missed providing :command:`pip3`,
alongside :command:`python3`,
please check your vendor's or distribution's software repository
for a package called `pip3` or `python3-pip`.
If this is not provided, please refer to the
`pip homepage <https://pip.pypa.io/en/stable/installing/>`_ for help.


Optionally you might want to install `PyPDF2`, `PyQt5` and
`python-poppler-qt5`
- which are requirements for |flyer-composer| -
provided by your distribution or vendor,
so at least these package will be maintained by your distribution.
Check for packages named ``python3-pypdf2``,
``python3-qt5-widgets``,
``python3-qt5-gui``,
``python3-qt5-network``,
``python3-qt5-xml``,
``python3-poppler-qt5``,
or that like.


Then continue with :ref:`installing flyer-composer` below.


.. _installing flyer-composer:

Installing |flyer-composer| using :command:`pip3`
-----------------------------------------------------------

After installing `Python` (and optionally the other required packages),
just run::

  sudo pip3 install flyer-composer

to install |flyer-composer| for all users.
For installing |flyer-composer| for yourself only, run::

  pip3 install --user flyer-composer


If your system does not have network access
----------------------------------------------

.. note:: Installation of  poppler and python-poppler-qt5 is missing here.

1) Download

   - |flyer-composer| from https://pypi.org/project/flyer-composer/,
   - `PyPDF2` from https://pypi.org/project/PyPDF2/,
   - `PyQt5` from https://pypi.org/project/PyQt5/ (pick the ``.whl`` file),
     and
   - `python-poppler-qt5` from https://pypi.org/project/python-poppler-qt5/
     (again, pick the ``.whl`` file).

2) Run ::

     sudo pip3 install flyer-composer-*.tar.gz PyPDF2-*.tar.gz \
               PyQt5-*.whl

   respective ::

     pip3 install --user flyer-composer-*.tar.gz PyPDF2-*.tar.gz PyQt5-*.whl


.. include:: _common_definitions.txt

