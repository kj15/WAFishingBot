import sys, os, django, datetime


abspath = os.path.abspath('../../gofish')
sys.path.append(abspath)

os.environ['DJANGO_SETTINGS_MODULE'] = 'gofish.settings'
django.setup()
from app.models import Lake, LakeStats


def get_stats():
    lakes = Lake.objects.all()
    find = LakeStats.objects.all()
    size = []
    alt = []
    if len(find) > 0:
        stats = find[0]
    else:
        stats = LakeStats()
    for lake in lakes:
        size.append(lake.size)
        alt.append(lake.altitude)
    for x in ['size', 'alt']:
        stats['min_' + x] = int(min(eval(x)))
        stats['avg_' + x] = int(sum(eval(x)) / len (eval(x)))
        stats['max_' + x] = int(max(eval(x)))
    stats.save()


if __name__ == '__main__':
    get_stats()