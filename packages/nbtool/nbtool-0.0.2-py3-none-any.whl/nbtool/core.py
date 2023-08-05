import sys
import subprocess
import yaml
from . import docker
from . import project
from . import freeze
from . import release
import os
from os import path

modules = {
    'docker': docker,
    'project':project ,
    'freeze':freeze,
    'release':release,
}

def help(args):
     
    if len(args) == 0:
        print('''
        welcome to nbtool help!
        to run nbtools:
        nb <cmd> args... (cmds: project|docker|release|freeze)
        nb help <cmd> to view help info for individual cmd
        
        workdir: nb will detect project root (where .nb.yaml file is stored)
        for most commands. (except for project config & init see nb help project)
        config-file: nb works with .nb.yaml at project root, if you have not configured such file, please run `nb project config`
        
        nb could read `gcloud info` automatically and determine your current project. it will respect `project` configuration in .nb.yaml if present though.
        
        nb assumes (init on demand) following project folder structure:
        .nb.yaml Dockerfile src chart README.md ... 
        folders:
            src: contains all source code.
            chart: contains helm chart to release/upgrade the service. see `nb help relase`
        
        ''')
        sys.exit(0)
    elif args[0] in modules:
        modules[args[0]].help()
    else:
        exit('there is no help for command: {0}'.format(args[0]))
    


def shell(cmds, stdout=False):
    sto = None
    if not stdout:
        sto = subprocess.PIPE
    p = subprocess.Popen(cmds,stdout=sto,shell=True)
    (out,err) = p.communicate()
    return p.returncode,out

def exit(err):
    print(err, file=sys.stderr)
    sys.exit(1)

    
    sys.exit(0)

def parse_gcloud():
    gcloud = {}
    r,o = shell(['gcloud info'])
    if r != 0:
        exit('gcloud sdk not installed or configured properly')
    lines = o.splitlines()
    for line in lines:
        line = str(line)
        if line.find('project:') != -1:
            p = line[line.find('[')+1:line.find(']')]
            if len(p) == 0:
                print('WARNING: gcloud has no project info, please try reconfigure gcloud')
            gcloud['project'] = p
            break
    return gcloud

def cd_project_root():
    ok = False
    while not ok:
        if path.abspath(os.curdir) == '/':
            exit('we failed to locate project root. maybe you have not run nb project config?')
        if not path.exists('.nb.yaml'):
            os.chdir('..')
        else:
            break
    print('working at {0}'.format(path.abspath(os.curdir)))
    

if __name__ == '__main__':
    if len(sys.argv) == 1:
        help([])

    cmd = str(sys.argv[1])
    if cmd == 'help':
        help(sys.argv[2:])
    if cmd not in modules:
        exit('cmd {0} not supported yet'.format(cmd)) 
    try:
        modules[cmd].handle(sys.argv[2:])
    except Exception as e:
        print(e)
        exit('{0} cmd faied to run'.format(cmd))
    
        
    
