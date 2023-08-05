Ursa-Major
==========

.. image:: https://img.shields.io/pypi/v/ursa-major.svg
   :alt: PyPI

.. image:: https://img.shields.io/pypi/l/ursa-major.svg
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/pyversions/ursa-major.svg
   :alt: PyPI - Python Version

Ursa-Major is a utility to help managing module's koji tags in koji's
inheritance. It reads configuration for tags from a tag config file, then
update koji's inheritance accordingly.

Tag Config File
---------------

The tag config file used by Ursa-Major is in json format, the top level keys
are koji tags which we should add module tags into their inheritance. For each
tag, it contains a list of modules, owners can also be set for a tag.

An example tag config file is:

.. code-block:: json

    {
        "fedora-30-buildroot-modules": {
            "modules": [
                {
                    "name": "httpd",
                    "priority": 10,
                    "buildrequires": {
                        "platform": "f30"
                    },
                    "requires": {
                        "platform": "f30"
                    },
                    "stream": "2.4"
                },
                {
                    "name": "ruby",
                    "priority": 40,
                    "requires": {
                        "platform": "f30"
                    },
                    "stream": "2.5"
                }
            ],
            "owners": [
                "foo@example.com"
            ]
        },
        "fedora-30-test-build": {
            "modules": [
                {
                    "name": "testmodule",
                    "priority": 150,
                    "stream": "f30"
                }
            ],
            "owners": [
                "bar@example.com"
            ]
        }
    }


A valid module config should contains:

* ``name`` (required): module name
* ``stream`` (required): module stream
* ``priority`` (required): add module's tag to tag inheritance with this priority
* ``requires`` (optional): module's runtime dependencies.
* ``buildrequires`` (optional): module's build time dependencies.

For each tag, ``owners`` can be set with email addresses.

The default tag config file used by Ursa-Major is ``ursa-major.json`` in current
working directory. You can change it with ``--tag-config-file``.


Koji and MBS
------------

Tags in tag config file are koji tags, Ursa-Major connects to koji hub and
update tag inheritance per config, and connects to MBS to query module's
information, especially the modulemd data.

Koji and MBS servers are set in Ursa-Major's config files, the global config
file is ``/etc/ursa-major/ursa-major`` by default, and can be changed by
``--config`` argument. The user config file is
``~/.config/ursa-major/ursa-major.conf``, and can be changed by
``--user-config``. User config file is optional, and values in global config
file will be overrided by user config file.

An example config file:

.. code-block:: bash

    $ cat /etc/ursa-major/ursa-major.conf

    [main]
    # See https://docs.python.org/3/library/logging.html#logging-levels
    log_level = info

    [koji]
    profile = koji

    [mbs]
    server_url = https://mbs.fedoraproject.org/

    [mail]
    mail_processing = true
    mail_log_level = info
    mail_server = smtp.example.com
    mail_from = ursa-major@example.com
    mail_replyto = ursa-major@example.com
    # email addresses seperated by ','
    mail_always_cc = ursa-major-admin@example.com
    mail_always_bcc =
    mail_subject_prefix = [ursa-major]


Sub Commands
============

Global arguments of ``ursa-major``:

* ``--debug`` (optional): print debug messages

* ``--dry-run`` (optional): run in dry-run mode, not do any real change

* ``--config`` (optional): default if ``/etc/ursa-major/ursa-major.conf``

* ``--user-config`` (optional): default is ``~/.config/ursa-major/ursa-major.conf``

* ``--tag-config-file`` (optional): default is ``$PWD/ursa-major.json``


show-config
-----------

This just show the content of tag config file, or the content of a specified
tag.

Arguments:

* ``--tag`` (optional): only show config content under this tag

Example:

.. code-block:: bash

    $ ursa-major show-config --tag-config-file ~/fedora-prod-ursa-major.json --tag fedora-30-test-build

check-config
------------

Check the tag config file to detect any invalid configuration:

.. code-block:: bash

    $ ursa-major check-config --tag-config-file ~/fedora-prod-ursa-major.json

Checks include:

* ``name``, ``stream`` and ``priority`` are required for a module
* ``priority`` value should not conflict with other parent tags which not belong
  to this module in tag's inheritance
* ...

remove-module
-------------

Remove a module from the tag config file.

Arguments:

* ``--tag`` (required): remove module from this tag

* ``--name`` (required): module name

* ``--stream`` (required): module stream

* ``--require`` (optional): module's runtime requires, can be specified multiple times

* ``--buildrequire`` (optional): module's buildrequires, can be specified multiple times


Example:

.. code-block:: bash

    $ ursa-major remove-module --tag fedora-30-test-build --name testmodule --stream f30

This will remove the module of ``testmodule:f30`` from tag config file if it's
s present under tag ``fedora-30-test-build``.

add-module
----------

Add a module to tag config file under the specified tag.

Arguments:

* ``--tag`` (required): add module to this tag

* ``--name`` (required): module name

* ``--stream`` (required): module stream

* ``--priority`` (required): priority value when add tag to inheritance

* ``--require`` (optional): module's runtime requires, can be specified multiple times

* ``--buildrequire`` (optional): module's buildrequires, can be specified multiple times

Example:

.. code-block:: bash

    $ ursa-major add-module --tag fedora-30-test-build --name testmodule --stream f30 --priority 100

If the specified module with that ``name`` and ``stream`` already exists in tag
config file, Ursa-Major will check whether ``requires`` or ``priority`` is
different from the value specified in command line, if true, the tag config
file will be updated to use the values specified.

update-tag
----------

Update a tag's inheritance data with all latest module build tags of the
modules in tag's config.

Arguments:

* ``--tag`` (required): the tag to update
* ``--wait-regen-repo`` (optional): wait for regen-repo task to finish

Example:

.. code-block:: bash

    $ ursa-major update-tag --tag fedora-30-test-build --wait-regen-repo

This will check the latest builds in MBS for all modules in config of tag
'fedora-30-test-build', if there is any build's tag is missing from tag's
inheritance data, the tag will be added into inheritance, and old tags
will be removed at the same time for the module.

add-tag
-------

Reads module state change message from an environment variable and then add
the module's koji tag tag inheritance according to tag config file if the
module build state is 'ready', and remove old tags of the module at the same
time. The module's state change message is generated by MBS.

Arguments:

* ``--module-from-env`` (optional): the environment variable Ursa-Major read the
  module state change message from, by default it's ``CI_MESSAGE``

* ``--wait-regen-repo`` (optinal): wait for regen-repo tasks to finish, default is ``False``

* ``--send-mail`` (optional): send mail to tag owners, default is ``False``

Example:

.. code-block:: bash

    $ cat $CI_MESSAGE
    {
      "state_reason": null,
      "component_builds": [
        108146,
        108145
      ],
      "name": "testmodule",
      "stream": "master",
      "time_submitted": "2018-10-26T16:59:06Z",
      "version": "20181026165847",
      "time_modified": "2018-10-26T16:59:27Z",
      "state_name": "ready",
      "scmurl": "https://src.fedoraproject.org/modules/testmodule.git?#3f262deef9d79160ea229142aeb51eedcc956929",
      "state": 5,
      "time_completed": "2018-10-26T16:59:15Z",
      "koji_tag": "module-testmodule-master-20181026165847-a5b0195c",
      "context": "a5b0195c",
      "owner": "foobar",
      "siblings": [],
      "id": 2321,
      "rebuild_strategy": "only-changed"
    }

    $ cat $PWD/ursa-major.json
    {
        "fedora-30-test-build": {
            "modules": [
                {
                    "name": "testmodule",
                    "priority": 150,
                    "stream": "master"
                }
            ],
            "owners": [
                "foobar@example.com"
            ]
        }
    }

    $ ursa-major add-tag --wait-regen-repo --send-mail

In this example, Ursa-Major reads the module state change message from
enviroment variable ``CI_MESSAGE``, the module build state name is "ready" and
module is present under a tag "fedora-30-test-build" in tag config file.
Ursa-Major will add the koji tag "module-testmodule-master-20181026165847-a5b0195c"
into "fedora-30-test-build"'s inheritance, and then regen-repo for build tags
in "fedora-30-test-build"'s inheritance.

When a tag is added to tag inheritance, Ursa-Major also submit ``regen-repo``
tasks for the build tags in inheritance data. If the specified tag is a build
tag, it's the only one build tag Ursa-Major will regen-repo for. Or Ursa-Major
will check the tag's inheritance data, if it reaches the first build tag in
each inheritant path, it returns that build tag. And it stops at any tag that
name starts with 'module-'.

For example, if we have tag inheritance data as below (tags with
'*' marks are build tags):

Example #1:

::

        my-example-tag
          └─product-foo-temp-override
             └─product-foo-override
                └─product-foo-build (*)
                   ├─tmp-product-foo-build (*)
                   └─alt-product-foo-build (*)

In this case, there is one build tag found for 'my-example-tag', it is:
``product-foo-build``. Ursa-Major stops at 'product-foo-build', so
'tmp-product-foo-build' and 'alt-product-foo-build' are not checked at all.

Example #2:

::

    my-example-tag
      ├─module-345678-build
      ├─module-234567-build
      ├─module-123456-build
      │  └─product-foo-module-hotfix
      │     └─product-foo-module-hotfix-build (*)
      ├─tmp-product-foo-python-candidate
      │  └─tmp-product-foo-python-override
      │     └─tmp-product-foo-python-build (*)
      ├─product-foo-container-build (*)
      └─product-foo-temp-override
         └─product-foo-override
            └─product-foo-build (*)
               ├─tmp-product-foo-build (*)
               └─alt-product-foo-build (*)

In this case, there are 3 build tags found for ``my-example-tag``, they are:
``tmp-product-foo-python-build``, ``product-foo-container-build`` and
``product-foo-build``. ``product-foo-module-hotfix-build`` is a build tag, but
Ursa-Major doesn't count it in, because it stops at tag 'module-123456-build'
which name starts with 'module-'.

Ursa-Major will send mail to tag owners if run with "--send-mail", mail
configuration can be configured in global config file or user config file,
under the section of "mail".
