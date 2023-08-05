# See LICENSE file for details
import sys
import os
import shutil
import git
import yaml
import logging

from repomanager.log import *
from repomanager.utils import *
from repomanager.constants import *
from repomanager.__init__ import __version__

def rpm(verbose, dir, clean, repolist, update, apply):

    #logger.level(getattr(logging, verbose.upper(), None))
    # Set up the logger
    setup_logging(verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(ColoredFormatter())
    logger.addHandler(ch)
    fh = logging.FileHandler('run.log', 'w')
    logger.addHandler(fh)

    logger.info('****** Repo Manager {0} *******'.format(__version__ ))
    logger.info('Copyright (c) 2020, InCore Semiconductors Pvt. Ltd.')
    logger.info('All Rights Reserved.')
    
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
                    # TODO
                    logger.warning('[update] {0} already exists'.format(repo_name))
            else:
                logger.info('[update] Cloning {0} ...'.format(repo_name))
                git.Repo.clone_from(repo_git, repo_name, branch=repo_branch, recursive=True)
                repo = git.Repo(repo_name)
                if commit_id:
                    repo_commit = str(repo.commit(repo_branch))
                    if(repo_commit != commit_id):
                        os.chdir('{0}'.format(workdir+'/' + repo_name))
                        sys_command('git checkout {0}'.format(repo_list[repo_name]['commitid']), logger)
                        os.chdir(workdir)
        if os.path.isdir(repo_dir):
            repo = git.Repo(repo_dir)
            repo_diff = repo.git.diff(None)
            repo_commit = str(repo.commit(repo_branch))
           
            if commit_id:
                if repo_commit != commit_id:
                    logger.debug('Commit ids of repo and the repo list yaml for {0} does not match. Possible patch/unpatch errors'.format(repo_name))

            if (apply == 'patch'):
                if 'patch' in repo_list[repo_name]:
                    if repo_list[repo_name]['patch']:
                        repo_patch = repo_list[repo_name]['patch']
                        for rp in repo_patch:
                            patch_path = repo_dir + '/' + rp[0]
                            repo_patched = git.Repo(patch_path)
                            patch_file = pwd + '/' + rp[1]
                            repo_diff = repo_patched.git.diff(None)
                            with open(patch_file, "r") as pf_handle:
                                patch_diff = pf_handle.read()
                            pf_handle.close()
                            if repo_diff.strip():
                                if repo_diff.strip() == patch_diff.strip():
                                    logger.warning('[patch] {0} already applied {1}/{2}'.format(rp[1], repo_name, rp[0]))
                                else:
                                    try:
                                        repo_patched.git.apply(['-R', '--check', patch_file])
                                        logger.warning('[patch] {0} present in  {1}/{2}'.format(rp[1], repo_name, rp[0]))
                                    except:
                                        try:
                                            print(repo_patched.apply(patch_file))
                                            logger.info('[patch] Repo diff seen: Applying {0} to {1}/{2}'.format(rp[1],repo_name, rp[0]))
                                        except:
                                            print(repo_patched.apply(patch_file))
                                            logger.error('[patch] Unsuccessful; {0} dirty'.format(repo_name))
                            else:
                                try:
                                    repo_patched.git.apply(patch_file)
                                    logger.info('[patch] Applying {0} to {1}/{2}'.format(rp[1],repo_name, rp[0]))
                                except:
                                    logger.error('[patch] Unsuccessful; Check diff')
            elif(apply == 'unpatch'):
                if 'patch' in repo_list[repo_name]:
                    if repo_list[repo_name]['patch']:
                        repo_patch = repo_list[repo_name]['patch']
                        for rp in repo_patch:
                            patch_path = repo_dir + '/' + rp[0]
                            repo_patched = git.Repo(patch_path)
                            patch_file = pwd + '/' + rp[1]
                            repo_diff = repo_patched.git.diff(None)
                            if repo_diff.strip():
                                try:
                                    repo_patched.git.apply(['--check', patch_file])
                                    logger.warning('[unpatch] {0} has nothing to unpatch'.format(repo_name))
                                except:
                                    try:
                                        repo_patched.git.apply(['-R', patch_file])
                                        logger.info('[unpatch] Removing {0} from {1}/{2}'.format(rp[1],repo_name, rp[0]))
                                    except:
                                        logger.error('[unpatch] Unsuccessful; repo dirty')
                            else:
                                logger.warning('[unpatch] {0} clean; has nothing to unpatch'.format(repo_name))

    logger.info('**********************************')

