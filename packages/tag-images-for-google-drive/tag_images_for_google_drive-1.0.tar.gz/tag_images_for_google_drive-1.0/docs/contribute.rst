.. index:: clone

Contribute
==========

The code use Conda_ , because we want some dependencies other than Python.

.. _Conda: https://www.anaconda.com/

Download sources

.. code-block:: bash

    $ git clone |giturl| tag_images_for_google_drive

then:

On Windows, use the Ubuntu subsystem, then install minicoda:

.. code-block:: bash

    $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    $ .//Miniconda3-latest-Linux-x86_64.sh

then:
.. code-block:: bash

    $ cd tag_images_for_google_drive
    $ conda install -y -c anaconda make
    $ make configure
    $ conda activate tag_images_for_google_drive
    $ make installer


* A ``make validate`` is executed before a ``git push`` in branch ``master``.
  It possible to force the push with ``FORCE=y git push``.
