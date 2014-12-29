
"""
setup django environment 
"""
import os,sys, getopt, django
prj_home = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
print "project home:", prj_home
sys.path.append(prj_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ndcloudV2.settings'
django.setup()


"""
program start here
"""
from core.models import *
import core.utils as utils


def main():
    submit_projects = getSubmittedProjects()
    if submit_projects != None:
        for project in submit_projects:
            runosm(project.id)
            project.status = utils.ProjectStatus.success
            project.threedmodel = "normal.obj"
            project.texture = "normal.obj.mtl"
            project.save()


def runosm(projectId):
    picdir = prj_home + "/medias/upload/%d/original" %(projectId)
    modeldir = prj_home + "/medias/upload/%d/original_models/" %(projectId)
    cmd = "sh /home/ubuntu/dev/program/osm-bundler-python/runosm.sh " + picdir
    os.system(cmd)
    cmd = "cp /home/ubuntu/dev/program/osm-bundler-python/final/normal.* "+modeldir
    os.system(cmd)
    


def getSubmittedProjects():
    submit_projects = ProjectProfile.objects.filter(status=utils.ProjectStatus.submit)
    print "submit projects:", submit_projects
    return submit_projects
    
    

if __name__ == '__main__':
    main()