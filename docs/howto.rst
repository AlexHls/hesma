How To - Project Documentation
======================================================================

Get Started
----------------------------------------------------------------------

Documentation can be written as rst files in `hesma/docs`.


To build and serve docs, use the commands::

    docker compose -f local.yml up docs



Changes to files in `docs/_source` will be picked up and reloaded automatically.

`Sphinx <https://www.sphinx-doc.org/>`_ is the tool used to build documentation.

Docstrings to Documentation
----------------------------------------------------------------------

The sphinx extension `apidoc <https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html/>`_ is used to automatically document code using signatures and docstrings.

Numpy or Google style docstrings will be picked up from project files and available for documentation. See the `Napoleon <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/>`_ extension for details.

For an in-use example, see the `page source <_sources/users.rst.txt>`_ for :ref:`users`.

To compile all docstrings automatically into documentation source files, use the command:
    ::

        make apidocs


This can be done in the docker container:
    ::

        docker run --rm docs make apidocs


Database Documentation
----------------------------------------------------------------------

To backup the database, use the command::

    export POSTGRES_BACKUP_DIR=<backup_dir>
    ./scripts/backup_local.sh

For the production enviroment use the ``backup_production.sh`` script instead.

Restore the database from a backup file::

    cat <backup_file> | docker exec -i hesma_local_postgres psql -U $POSTGRES_USER -d postgres

The ``$POSTGRES_USER`` is set in the ``.envs/.local/.postgres`` file.
For the production enviroment the database name and user have to be adapted.

To enable the database backup as a cron job, add the following line to the crontab (e.g. ``/etc/crontab`` or ``/var/spool/cron/username``)::

    0 2 * * * /path/to/backup_production.sh

This will backup the database every day at 2am.
Alternatively, create an executable file in ``/etc/cron.daily`` with the content::

    #!/bin/sh
    export POSTGRES_BACKUP_DIR=/path/to/backup/dir
    /path/to/backup_production.sh
