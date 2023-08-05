import sys
from . import core
from . import project

def help():
    print('available commands: build')
    sys.exit(0)


def handle(args):
    if len(args) == 0:
        help()
    cmd = args[0]
    if 'build'.find(cmd) == 0:
        print('running docker build')
        p = project.load()
        version = p[project.key_version]
        crhost= p[project.key_crhost]
        image = p[project.key_image]
        prj = p[project.key_project]
        docker_tag = '{0}/{1}/{2}:{3}'.format(crhost,prj,image,version)
        shell_cmd = 'docker build -t {0} .'.format(docker_tag)
        print(shell_cmd)
        r,o = core.shell(shell_cmd, stdout=True)
        if r!=0:
            core.exit('error while building docker image')
        r,o = core.shell('git tag')
        if len(o) == 0:
           core.exit('skipped uploading on un-tagged revision') 
        if r != p[project.key_version]:
           core.exit('skipped uploading because tag:{0} and version:{1} not matching'.format(r, version)) 
        core.shell('docker push {0}'.format(docker_tag))
        pass       
    else:
        core.exit('invalid command : {0}'.format(cmd))
        
