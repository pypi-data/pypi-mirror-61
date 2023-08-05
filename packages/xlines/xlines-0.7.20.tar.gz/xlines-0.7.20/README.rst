 \* \* * # xlines * \* \*

Summary
-------

Count the number of lines of text in a code project (or anything else)

**Version**: 0.7.19

--------------

Contents
--------

-  `**Dependencies** <#dependencies>`__

-  `**Program Options** <#program-options>`__

-  `**Build Options** <#build-options>`__

-  `**Configuration** <#configuration>`__

-  `**Exclusions** <#exclusions>`__

-  `**Installation** <#installation>`__

   -  `Pip Install <#installation>`__
   -  `Ubuntu, Linux Mint, Debian-based
      Distributions <#debian-distro-install>`__
   -  `Redhat, CentOS <#redhat-distro-install>`__
   -  `Amazon Linux 2, Fedora <#amzn2-distro-install>`__

-  `**Screenshots** <#screenshots>`__

-  `**Author & Copyright** <#author--copyright>`__

-  `**License** <#license>`__

-  `**Disclaimer** <#disclaimer>`__

--

`back to the top <#top>`__

--------------

Dependencies
------------

`xlines <https://github.com/fstab50/xlines>`__ requires `Python
3.6+ <https://docs.python.org/3/>`__.

If your environment has Python 3.5 or older or is missing Python 3
altogether, consider using nlines as an excellent alternative. nlines
`bash <https://www.gnu.org/software/bash>`__ implementation line counter
is compatible with virtually any Linux-based development environment.

`back to the top <#top>`__

--------------

Program Options
---------------

To display the **xlines** help menu:

.. code:: bash

        $ xlines --help

.. raw:: html

   <p align="center">

::

    <a href="http://images.awspros.world/xlines/help-menu.png" target="_blank"><img src="./assets/help-menu.png">

.. raw:: html

   </p>

--

`back to the top <#top>`__

--------------

Build options
-------------

**`GNU Make <https://www.gnu.org/software/make>`__ Targets**. Type the
following to display the available make targets from the root of the
project:

.. code:: bash

        $  make help

.. raw:: html

   <p align="center">

::

    <a href="http://images.awspros.world/xlines/make-help.png" target="_blank"><img src="./assets/make-help.png">

.. raw:: html

   </p>

--

`back to the top <#top>`__

--------------

Configuration
-------------

Configure `xlines <https://github.com/fstab50/xlines>`__ runtime options
by entering the configuration menu:

.. code:: bash

        $ xlines --configure

|toc| 

`back to the top <#top>`__

--

Option "A" (shown below) allows addition of file types to be excluded
(skipped) from line totals

|option a|

`back to the top <#top>`__

--

Option "B" (shown below) allows deletion of file types from the
exclusion list so that a specific file extension will be included in
total line counts:

|option b| 

`back to the top <#top>`__

--

Option "C" (shown below) allows user-customization of files highlighted
for containing a large number of lines of text:

|option c|

--

`back to the top <#top>`__

--------------

Installation
------------

--------------

Pip Install
~~~~~~~~~~~

**xlines** may be installed on Linux via `pip, python package
installer <https://pypi.org/project/pip>`__ in one of two methods:

To install **xlines** for a single user:

::

    $  pip3 install xlines --user

To install **xlines** for all users (Linux):

::

    $  sudo -H pip3 install xlines

`back to the top <#top>`__

--------------

 ### Ubuntu, Linux Mint, Debian variants (Python 3.6, 3.7)

The easiest way to install **xlines** on debian-based Linux
distributions is via the debian-tools package repository:

1. Open a command line terminal.

   |deb-install0|

2. Download and install the repository definition file

   ::

       $ sudo apt install wget

   ::

       $ wget http://awscloud.center/deb/debian-tools.list

   |deb-install1|

   ::

       $ sudo chown 0:0 debian-tools.list && sudo mv debian-tools.list /etc/apt/sources.list.d/

3. Install the package repository public key on your local machine

   ::

       $ wget -qO - http://awscloud.center/keys/public.key | sudo apt-key add -

   |deb-install2|

4. Update the local package repository cache

   ::

       $ sudo apt update

5. Install **xlines** os package

   ::

       $ sudo apt install python3-xlines

   Answer "y":

   |deb-install3|

6. Verify Installation

   ::

       $ apt show python3-xlines

   |rpm-install4|

`back to the top <#top>`__

--------------

 ### Redhat, CentOS (Python 3.6)

The easiest way to install **xlines** on redhat-based Linux
distributions is via the developer-tools package repository:

1. Open a command line terminal.

   |rpm-install0|

2. Install the official epel package repository

   ::

       $ sudo yum install epel-release

3. Download and install the repo definition file

   ::

       $ sudo yum install wget

   |rpm-install1|

   ::

       $ wget http://awscloud.center/rpm/developer-tools.repo

   |rpm-install2|

   ::

       $ sudo chown 0:0 developer-tools.repo && sudo mv developer-tools.repo /etc/yum.repos.d/

4. Delete the local repository cache, then Update the cache with new
   package references

   ::

       $ sudo rm -fr /var/cache/yum
       $ sudo yum update -y

5. Install the **python3-xlines** os package

   ::

       $ sudo yum install python36-xlines

   |rpm-install3|

   Answer "y":

   |rpm-install4|

6. Verify Installation

   ::

       $ yum info python36-xlines

   |rpm-install5|

`back to the top <#top>`__

--------------

 ### Amazon Linux 2 / Fedora (Python 3.7)

The easiest way to install **xlines** on redhat-based Linux distribution
`Amazon Linux 2 <https://aws.amazon.com/amazon-linux-2>`__ or
`Fedora <http://fedoraproject.org>`__, is via the developer-tools
`amzn2.awscloud.center <http://amzn2.awscloud.center>`__ package
repository:

1. Install the official epel package repository

   ::

       $ sudo amazon-linux-extras install epel -y

2. Download and install the repo definition file

   ::

       $ sudo yum install wget

   |amzn2-install1|

   ::

       $ wget http://awscloud.center/amzn2/developer-tools.repo

   |amzn2-install2|

   ::

       $ sudo chown 0:0 developer-tools.repo && sudo mv developer-tools.repo /etc/yum.repos.d/

3. Delete the local repository cache, then Update the cache with new
   package references

   ::

       $ sudo rm -fr /var/cache/yum
       $ sudo yum update -y

4. Install **xlines** os package

   ::

       $ sudo yum install python37-xlines

   |amzn2-install3|

   Answer "y":

   |amzn2-install4|

5. Verify Installation

   ::

       $ yum info python37-xlines

   |rpm-install5|

   A check of python3 should point to Python 3.7:

   ::

       $ python3 --version

   ::

       $ Python 3.7.X

--

`back to the top <#top>`__

--------------

Screenshots
-----------

Project 1: Line count, low complexity git repository:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

        $ xlines  --sum  git/branchdiff

.. raw:: html

   <p align="center">

::

    <a href="http://images.awspros.world/xlines/xlines-output-branchdiff.png"><img src="./assets/xlines-output-branchdiff-md.png" width="900">

.. raw:: html

   </p>

`back to the top <#top>`__

--------------

Project 2: Line count, medium complexity git repository:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <p align="right">

::

    <a href="http://images.awspros.world/xlines/xlines-awslabs.png"><img src="./assets/awslabs-content.png">

.. raw:: html

   </p>

`back to the top <#top>`__

--------------

Project 3: Line count, high complexity git repository:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <p align="right">

::

    <a href="http://images.awspros.world/xlines/xlines_output_large.png"><img src="./assets/awslabs-serverless.png">

.. raw:: html

   </p>

`back to the top <#top>`__

--------------

Author & Copyright
------------------

All works contained herein copyrighted via below author unless work is
explicitly noted by an alternate author.

-  Copyright Blake Huber, All Rights Reserved.

`back to the top <#top>`__

--------------

License
-------

-  Software contained in this repo is licensed under the `license
   agreement <./LICENSE.md>`__. You may display the license and
   copyright information by issuing the following command:

::

    $ xlines --version

|help|

`back to the top <#top>`__

--------------

Disclaimer
----------

*Code is provided "as is". No liability is assumed by either the code's
originating author nor this repo's owner for their use at AWS or any
other facility. Furthermore, running function code at AWS may incur
monetary charges; in some cases, charges may be substantial. Charges are
the sole responsibility of the account holder executing code obtained
from this library.*

Additional terms may be found in the complete `license
agreement <./LICENSE.md>`__.

`back to the top <#top>`__

--------------

.. |toc| image:: ./assets/configure_toc.png
   :target: http://images.awspros.world/xlines/configure_toc.png
.. |option a| image:: ./assets/configure_a.png
   :target: http://images.awspros.world/xlines/configure_a.png
.. |option b| image:: ./assets/configure_b.png
   :target: http://images.awspros.world/xlines/configure_b.png
.. |option c| image:: ./assets/configure_c.png
   :target: http://images.awspros.world/xlines/configure_c.png
.. |deb-install0| image:: ./assets/deb-install-0.png
   :target: http://images.awspros.world/xlines/deb-install-0.png
.. |deb-install1| image:: ./assets/deb-install-1.png
   :target: http://images.awspros.world/xlines/deb-install-1.png
.. |deb-install2| image:: ./assets/deb-install-2.png
   :target: http://images.awspros.world/xlines/deb-install-2.png
.. |deb-install3| image:: ./assets/deb-install-3.png
   :target: http://images.awspros.world/xlines/deb-install-3.png
.. |rpm-install4| image:: ./assets/rpm-install-4.png
   :target: http://images.awspros.world/xlines/rpm-install-4.png
.. |rpm-install0| image:: ./assets/rpm-install-0.png
   :target: http://images.awspros.world/xlines/rpm-install-0.png
.. |rpm-install1| image:: ./assets/rpm-install-1.png
   :target: http://images.awspros.world/xlines/rpm-install-1.png
.. |rpm-install2| image:: ./assets/rpm-install-2.png
   :target: http://images.awspros.world/xlines/rpm-install-2.png
.. |rpm-install3| image:: ./assets/rpm-install-3.png
   :target: http://images.awspros.world/xlines/rpm-install-3.png
.. |rpm-install5| image:: ./assets/rpm-install-5.png
   :target: http://images.awspros.world/xlines/rpm-install-5.png
.. |amzn2-install1| image:: ./assets/amzn2-install-1.png
   :target: http://images.awspros.world/xlines/amzn2-install-1.png
.. |amzn2-install2| image:: ./assets/amzn2-install-2.png
   :target: http://images.awspros.world/xlines/amzn2-install-2.png
.. |amzn2-install3| image:: ./assets/amzn2-install-3.png
   :target: http://images.awspros.world/xlines/amzn2-install-3.png
.. |amzn2-install4| image:: ./assets/amzn2-install-4.png
   :target: http://images.awspros.world/xlines/amzn2-install-4.png
.. |rpm-install5| image:: ./assets/amzn2-install-5.png
   :target: http://images.awspros.world/xlines/amzn2-install-5.png
.. |help| image:: ./assets/version-copyright.png
   :target: https://s3.us-east-2.amazonaws.com/http-imagestore/xlines/version-copyright.png
