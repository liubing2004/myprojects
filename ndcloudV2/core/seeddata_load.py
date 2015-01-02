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


def loadPriceUnit():
    for pu in PriceUnit.objects.all():
        pu.delete()
    priceUnit = PriceUnit(price=10, material=utils.Material.plastic, 
                          color=utils.Color.white, unit=utils.SizeUnit.cm, finish="")
    priceUnit.save()
    priceUnit = PriceUnit(price=12, material=utils.Material.plastic, 
                          color=utils.Color.red, unit=utils.SizeUnit.cm, finish="")
    priceUnit.save()
    priceUnit = PriceUnit(price=0.01, material=utils.Material.plastic, 
                          color=utils.Color.white, unit=utils.SizeUnit.mm, finish="")
    priceUnit.save()
    priceUnit = PriceUnit(price=0.012, material=utils.Material.plastic, 
                          color=utils.Color.red, unit=utils.SizeUnit.mm, finish="")
    priceUnit.save()
    
def main():
    loadPriceUnit()
    
if __name__ == '__main__':
    main()