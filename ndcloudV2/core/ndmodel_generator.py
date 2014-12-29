
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
program starts here
"""
from core.models import *
import core.utils as utils

OSM_DIR = "/home/ubuntu/dev/program/osm-bundler-python/"
PIC_DIR_TEMPLATE = prj_home + "/medias/upload/%d/original/"
MODEL_DIR_TEMPLATE = prj_home + "/medias/upload/%d/original_models/"


def main():
    submit_projects = getSubmittedProjects()
    if submit_projects != None:
        for project in submit_projects:
            if runosm(project.id):
                project.status = utils.ProjectStatus.success
                project.threedmodel = "normal.obj"
                project.texture = "normal.obj.mtl"
                project.save()
            else:
                project.status = utils.ProjectStatus.fail
                project.save()


def runosm(projectId):
    picdir = PIC_DIR_TEMPLATE %(projectId)
    modeldir = MODEL_DIR_TEMPLATE %(projectId)
    cmd = "cd %s; sh runosm.sh %s; cd %s"  %(OSM_DIR, picdir, prj_home)
    os.system(cmd)
    cmd = "cp %sfinal/normal.*  %s" %(OSM_DIR, modeldir)
    os.system(cmd)
    if os.path.isfile("%sfinal/normal.obj" %(OSM_DIR)):
        return True
    return False
    


def getSubmittedProjects():
    submit_projects = ProjectProfile.objects.filter(status=utils.ProjectStatus.submit)
    print "submit projects:", submit_projects
    return submit_projects
    
    

if __name__ == '__main__':
    main()