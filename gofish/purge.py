import sys, os, django
# abspath = os.path.abspath('gofish')
# sys.path.append(abspath)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'gofish.settings'
django.setup()
from app.models import Lake, StockingData

if __name__ == '__main__':

    print "Are you sure? You better be goddamn sure (Y/N):"
    answer = raw_input()
    if str(answer).lower() == 'Y':
        Lake.objects.all().delete()
        StockingData.objects.all().delete()