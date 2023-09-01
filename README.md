# Hesma

Heidelberg Supernova Model Archive

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: GPLv3

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy hesma

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### File storage setup

Per default, all files will be stored in the ``MEDIA_ROOT`` directory in the default container volume. For larger files, it might be desirable to store them in a separate directory.
Specific directories for the different models can be setup by specifying e.g. the ``META_DATA_DIR`` in the respective ``.env`` file (relative paths will still be relative to the ``MEDIA_ROOT`` directory).
Additional volumes can be mounted following the standard Docker procedures.
In particular, if files should be stored in a location outside the container context, a bind mount has to be set up. (This might be desirable for extremely large files for which e.g. a backup is unfeasible.) To do so, add e.g. a

```yaml

    volumes:
      - .:/app:z # The default location. Do not remove
      - type: bind
        source: /path/to/docker_bind_vol
        target: /data
```

section to the django service of your compose file.
In the example above you would add ``META_DATA_DIR=/data/meta_data`` to your django ``.env`` file to store all meta data files in ``/path/to/docker_bind_vol/meta_data``.


### User groups

After the initial setup, some user groups need to be defined in the admin interface. If these groups are not set the upload sites will not work properly.
The groups that need to be set up are:
 - hydro_user
 - tracer_user
 - rt_user
