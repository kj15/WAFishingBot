import sys, os, django, datetime


abspath = os.path.abspath('../../gofish')
sys.path.append(abspath)

os.environ['DJANGO_SETTINGS_MODULE'] = 'gofish.settings'
django.setup()
from app.models import Lake, LakeStats


def get_stats():
    lakes = Lake.objects.all().filter(rank__gt=0.0)
    find = LakeStats.objects.all()
    size = []
    alt = []
    if len(find) > 0:
        stats = find[0]
    else:
        stats = LakeStats.objects.create()
    for lake in lakes:
        size.append(lake.size)
        alt.append(lake.altitude)
    for x in ['size', 'alt']:
        setattr(stats, 'min_' + x, min(eval(x)))
        setattr(stats, 'avg_' + x, sum(eval(x)) / len (eval(x)))
        setattr(stats, 'max_' + x, max(eval(x)))
    stats.total = len(lakes)
    stats.last_updated = datetime.date.today()
    stats.save()


if __name__ == '__main__':
    get_stats()