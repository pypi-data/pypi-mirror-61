import sys
import subprocess
import yaml
from . import docker
from . import project
from . import freeze
from . import release




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

def help():
    print('welcome to nbtool')
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

if __name__ == '__main__':
    cmds = {
                'docker': docker,
                'project':project ,
                'freeze':freeze,
                'release':release,
           }
    if len(sys.argv) == 1:
        help()

    cmd = str(sys.argv[1])
    if cmd not in cmds:
        exit('cmd {0} not supported yet'.format(cmd)) 
    try:
        cmds[cmd].handle(sys.argv[2:])
    except Exception as e:
        print(e)
        exit('{0} cmd faied to run'.format(cmd))
    
        
    
