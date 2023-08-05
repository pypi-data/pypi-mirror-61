from . import core
from sys import stdin
import yaml

key_crhost = 'crhost'
key_project = 'project'
key_image= 'image'
key_version= 'version'
key_service= 'k8s_service'


project_configs = {
    key_crhost : 'host for container registry',
    key_project: 'gcloud project',
    key_image: 'docker image name',
    key_version: 'version',
    key_service: 'k8s service name',
}


def help():
    print('''
        config or init a project
        config:
            nb project config
            NOTE: pls make sure you are running this at project root path
            as .nb.yaml file will be generated in here.
            You will be asked to configure typical nb project properties,
            don't worry in case some values are entered incorrectly,
            you could always edit .nb.yaml file after this step.
        init:
            nb project init
            to be implemented
    ''')
    core.exit('')

def load(check=True):
    c = {}
    for k in project_configs:
        if k not in c:
            c[k] = '' 
    try:
        with open('.nb.yaml','r') as f:
            l = yaml.load(f,Loader=yaml.BaseLoader)
            if l is not None:
                c = l
            if check:
                for k in project_configs:
                    if k not in c or len(c[k]) == 0:
                        core.exit('config:{0} not found'.format(k))
            return c
    except EnvironmentError:
        if check:
            core.exit('.nb.yaml not found in current path. maybe try nb project config?')
        return c

def do_config():
    print('config project')
    c = load(check=False)
    if key_project not in c:
        print('project configure not found, trying to retrive from gcloud sdk')
        g = core.parse_gcloud()
        c[key_project] = g['project']
    for k in project_configs:
        if k not in c:
            c[k] = ''
        atleast_once = True
        while len(c[k]) == 0 or atleast_once:
            atleast_once=False
            print('{0}? [{1}]'.format(project_configs[k],c[k])) 
            user = stdin.readline().strip()
            if len(user) == 0 and len(c[k]) != 0:
                # so we keep the original value
                break
            c[k] = user
    with open('.nb.yaml', 'w') as f:
        f.write(yaml.dump(c))    
    print('.nb.yaml configured')        

def do_init():
    pass
        

def handle(args):
    if len(args) == 0:
        help()
    cmd = args[0]
    if 'config'.find(cmd) == 0:
        do_config()
    elif 'init'.find(cmd) == 0:
        do_config()
        do_init()
        
