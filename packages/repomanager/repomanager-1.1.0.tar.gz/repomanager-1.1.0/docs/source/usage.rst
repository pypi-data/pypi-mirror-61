.. See LICENSE for details

Command Line Usage
======================

.. code-block:: bash

  $ repomanager --help
  Usage: repomanager [OPTIONS]
  
  Options:
    --version            Show the version and exit.
    -v, --verbose TEXT   Set verbose level
    -d, --dir PATH       Work directory path
    -c, --clean          Clean builds
    --repolist FILENAME  Repo list to be cloned
    -u, --update         Update Repo for specified branch
    -p, --patch          Apply patch to the repo
    -r, --unpatch        Remove patch from the repo
    --help               Show this message and exit.


.. code-block:: yaml

   
  <repo name>:
    repo: <git patch>
    checkout: <branch name>
    commitid: <if specific commit in branch>


Example yaml with checking out a particular commitid from master branch
########################################################################

.. code-block:: yaml

  aapg:
    repo: https://gitlab.com/shaktiproject/tools/aapg.git
    checkout: master
    commitid: e644b3bcb5a4640297c83206f74a7800665b92bb

Example yaml with checking out a particular tag
########################################################################
.. code-block:: yaml

  aapg:
    repo: https://gitlab.com/shaktiproject/tools/aapg.git
    checkout: 1.0.1
    commitid:
    patch: aapg.patch

Run repomanager
########################

.. code-block:: bash

  $ repomanager --repolist repolist.yaml -cup
