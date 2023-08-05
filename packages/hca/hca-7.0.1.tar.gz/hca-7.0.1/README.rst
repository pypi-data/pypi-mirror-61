HCA CLI
=======
This repository is a pip installable Command Line Interface (CLI) and Python library (API) for interacting with the
Data Coordination Platform (DCP) of the Human Cell Atlas (HCA).

Currently the `hca` package supports interaction with the `Upload Service <https://github.com/HumanCellAtlas/upload-service>`_ and `Data Storage Service (DSS) <https://github.com/HumanCellAtlas/data-store>`_ for services such as uploading, downloading,
and querying data.

The HCA CLI is compatible with Python versions 3.5+ (we are no longer compatible with Python 2.7, and our last compatible Python 2.7 version was `hca==6.4.0`).

Installation
------------
:code:`pip install hca`.

Usage
-----

Documentation on readthedocs.io:

* `CLI documentation <https://hca.readthedocs.io/en/latest/cli.html>`_

* `Python API documentation <https://hca.readthedocs.io/en/latest/api.html>`_

Example CLI/API usage:

* `CLI examples (open endpoints) <https://github.com/HumanCellAtlas/dcp-cli/tree/master/docs/OpenCLIExamples.rst>`_

* `CLI examples (restricted endpoints) <https://github.com/HumanCellAtlas/dcp-cli/tree/master/docs/RestrictedCLIExamples.rst>`_

* `Python API examples (open endpoints) <https://github.com/HumanCellAtlas/dcp-cli/tree/master/docs/OpenAPIExamples.rst>`_

* `Python API examples (restricted endpoints) <https://github.com/HumanCellAtlas/dcp-cli/tree/master/docs/OpenAPIExamples.rst>`_

To see the list of commands you can use, type :code:`hca --help`.

Configuration management
~~~~~~~~~~~~~~~~~~~~~~~~
The HCA CLI supports ingesting configuration from a configurable array of sources. Each source is a JSON file.
Configuration sources that follow the first source update the configuration using recursive dictionary merging. Sources
are enumerated in the following order (i.e., in order of increasing priority):

- Site-wide configuration source, ``/etc/hca/config.json``
- User configuration source, ``~/.config/hca/config.json``
- Any sources listed in the colon-delimited variable ``HCA_CONFIG_FILE``
- Command line options

**Array merge operators**: When loading a chain of configuration sources, the HCA CLI uses recursive dictionary merging
to combine the sources. Additionally, when the original config value is a list, the package supports array manipulation
operators, which let you extend and modify arrays defined in underlying configurations. See
https://github.com/kislyuk/tweak#array-merge-operators for a list of these operators.

Service to Service Authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Google service credentials must be whitelisted before they will authenticate with the HCA CLI.

Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of your Google service credentials file to
authenticate.

One can also use: ``hca dss login``.

See `Google service credentials <https://cloud.google.com/iam/docs/understanding-service-accounts>`_ 
for more information about service accounts. Use the `Google Cloud IAM web console
<https://console.cloud.google.com/iam-admin/serviceaccounts>`_ to manage service accounts.

Development
-----------
To develop on the CLI, first run ``pip install -r requirements-dev.txt``. You can install your locally modified copy of 
the hca package by running ``make install`` in the repository root directory.

To use the command line interface with a local or test DSS, first run ``hca`` (or ``scripts/hca`` if you want to use the
package in-place from the repository root directory). This will create the file ``~/.config/hca/config.json``, which you
can modify to update the value of ``DSSClient.swagger_url`` to point to the URL of the Swagger definition served by your
DSS deployment. Lastly, the CLI enforces HTTPS connection to the DSS API. If you are connecting to a local DSS, make
this change in ``dcp-cli/hca/util/__init__.py`` in the ``SwaggerClient`` object::

    scheme = "http"

To use the Python interface with a local or test DSS, pass the URL of the Swagger definition to the ``DSSClient``
constructor via the ``swagger_url`` parameter::

    client = DSSClient(swagger_url="https://dss.example.com/v1/swagger.json")

You can also layer a minimal config file on top of the default ``config.json`` using the ``HCA_CONFIG_FILE`` environment
variable, for example::

    export SWAGGER_URL="https://dss.staging.data.humancellatlas.org/v1/swagger.json"
    jq -n .DSSClient.swagger_url=env.SWAGGER_URL > ~/.config/hca/config.staging.json
    export HCA_CONFIG_FILE=~/.config/hca/config.staging.json

Testing
-------
Before you run tests, first run ``hca dss login``.  This will open a browser where you can log in to authenticate
with Google. Use an email address from one of the whitelisted domains (in ``DSS_SUBSCRIPTION_AUTHORIZED_DOMAINS_ARRAY``
from `here <https://github.com/HumanCellAtlas/data-store/blob/master/environment#L55>`_).

Then :code:`make test`.

Primary CI testing is through Travis CI; there is also additional testing with the
`Gitlab Allspark instance <https://allspark.dev.data.humancellatlas.org/HumanCellAtlas/dcp-cli/>`_ that runs tests for Windows.
(Note that Allspark is not open to the public, members of the Human Cell Atlas project can access the Allspark cluster using the Github account
associated with the Human Cell Atlas organization on Github.) If submitting PRs that have the potential of being platform-dependent, please ensure 
the status of "Windows Testing" is verified before merging.

Bugs
~~~~
Please report bugs, issues, feature requests, etc. in the 
`HumanCellAtlas/dcp-cli repository on GitHub <https://github.com/HumanCellAtlas/dcp-cli/issues>`_.


Security Policy
---------------
See our `Security Policy <https://github.com/HumanCellAtlas/.github/blob/master/SECURITY.md>`_.

License
-------
Licensed under the terms of the `MIT License <https://opensource.org/licenses/MIT>`_.

.. image:: https://img.shields.io/travis/HumanCellAtlas/dcp-cli.svg?branch=master
        :target: https://travis-ci.org/HumanCellAtlas/dcp-cli?branch=master
.. image:: https://codecov.io/github/HumanCellAtlas/dcp-cli/coverage.svg?branch=master
        :target: https://codecov.io/github/HumanCellAtlas/dcp-cli?branch=master
.. image:: https://img.shields.io/pypi/v/hca.svg
        :target: https://pypi.python.org/pypi/hca
.. image:: https://img.shields.io/pypi/l/hca.svg
        :target: https://pypi.python.org/pypi/hca
.. image:: https://readthedocs.org/projects/hca/badge/?version=latest
        :target: https://hca.readthedocs.io/
