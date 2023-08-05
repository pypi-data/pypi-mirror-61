# See LICENSE file for details
import sys
import os
import shutil
import git
import yaml
import logging

from repomanager.log import logger
from repomanager.utils import *
from repomanager.constants import *
from repomanager.__init__ import __version__

def rpm(verbose, dir, clean, repolist, update, apply):

    logger.level(getattr(logging, verbose.upper(), None))

    logger.info('****** Repo Manager {0} *******'.format(__version__ ))
    logger.info('Copyright (c) 2020, InCore Semiconductors Pvt. Ltd.')
    logger.info('All Rights Reserved.\n\n')
    
    repo_list = yaml.safe_load(repolist)
    pwd = os.getcwd() 
    workdir = pwd + '/' + dir 

    # clean gets priority
    if clean:
        for repo_name in repo_list:
            repo_dir = workdir + repo_name
            if os.path.isdir(repo_dir):
                shutil.rmtree(repo_dir, ignore_errors=True, onerror=None)
                logger.debug('[clean] {0} deleted'.format(repo_dir))

    for repo_name in repo_list:
        repo_dir = workdir + repo_name
        commit_id = repo_list[repo_name]['commitid']
        repo_branch = repo_list[repo_name]['checkout']
        repo_git = repo_list[repo_name]['repo']
        repo_patch = None
        if 'patch' in repo_list[repo_name]:
            if repo_list[repo_name]['patch'] is not None:
                repo_patch = pwd + '/' + repo_list[repo_name]['patch']
        if update:
            os.makedirs(workdir, exist_ok=True)
            os.chdir(workdir)
            if os.path.exists(repo_name):
                repo = git.Repo(repo_name)
                repo_commit = str(repo.commit(repo_branch))
                logger.debug(repo_commit)
                if commit_id:
                    if(repo_commit == commit_id):
                        logger.warning('[update] Repo {0} already exists'.format(repo_name))
                    else:
                        logger.warning('[update] todo: unpatch; git pull;checkout branch; checkout new commit; git submodule --init --recursive')
                else:
                    logger.warning('[update] {0} already exists'.format(repo_name))
            else:
                logger.info('[update] Cloning {0} ...'.format(repo_name))
                git.Repo.clone_from(repo_git, repo_name, branch=repo_branch)
                repo = git.Repo(repo_name)
                if commit_id:
                    repo_commit = str(repo.commit(repo_branch))
                    if(repo_commit != commit_id):
                        os.chdir('{0}'.format(workdir+'/' + repo_name))
                        sys_command('git checkout {0}'.format(repo_list[repo_name]['commitid']))
                        os.chdir(workdir)
                for submodule in repo.submodules:
                    submodule.update(init=True)
        if os.path.isdir(repo_dir):
            repo = git.Repo(repo_dir)
            repo_diff = repo.git.diff(None)
            repo_commit = str(repo.commit(repo_branch))
           
            if commit_id:
                if repo_commit != commit_id:
                    logger.debug('Commit ids of repo and the repo list yaml for {0} does not match. Possible patch/unpatch errors'.format(repo_name))

            if repo_patch:
                if (apply == 'patch'):
                    if not repo_diff:
                        logger.info('[patch] Applying patch:{0} to {1}'.format(repo_patch,repo_name))
                        repo.git.apply([repo_patch])
                    else:
                        logger.warning('[patch] Repo:{0} already has a patch; unpatch before using'.format(repo_name))
                elif(apply == 'unpatch'):
                    if not repo_diff:
                        logger.warning('[unpatch] Repo:{0} has nothing to unpatch'.format(repo_name))
                    else:
                        logger.info('[unpatch] Removing patch:{0} from {1}'.format(repo_patch,repo_name))
                        repo.git.apply(['-R', repo_patch])

