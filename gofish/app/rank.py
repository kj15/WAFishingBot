import sys, os, django, datetime
abspath = os.path.abspath('../../gofish')
sys.path.append(abspath)

os.environ['DJANGO_SETTINGS_MODULE'] = 'gofish.settings'
django.setup()
from app.models import Lake, StockingData

def rank_lakes():
    for lake in Lake.objects.all():
        print lake.name
        stocking = StockingData.objects.all().filter(lake=lake).order_by('date')
        if len(stocking) > 0:
            elev_rank = calc_elev_rank(lake)
            stocking_rank = calc_stocking(lake, stocking)
            rank = 2 * (elev_rank)**1./2. + stocking_rank
            lake.rank = round(rank, 3)
            lake.save()
        else:
            lake.rank = 0.0
            lake.save()

# calculates the rating for the altitude based on the time of year
def calc_elev_rank(lake):
    cd = float(datetime.datetime.now().timetuple().tm_yday)
    # gavin has some weird math thing where the currentday value begins at sep1 (0) and ends at aug31 (365)
    # so 244 -> 0 and 243 -> 365
    if cd >= 244:
        current_day = cd - 244
    else:
        current_day = 365 - abs(cd - 243)
    return 50000.0 / (abs(lake.altitude - (.1513 * current_day) ** 2 + 49.5 * current_day + 5254))

# calcualtes rating for the stocked fish vs the size of lake
def calc_stocking(lake, stocking):
    current_year = float(datetime.date.today().year)
    multiplier = len(stocking)
    ranks = []
    for s in stocking:
        stock_val = s.amount / (lake.size * (current_year - s.date.year)) * .2
        ranks.append(multiplier * stock_val)
        multiplier -= 1
    return reduce(lambda x,y: x + y, ranks) / len(ranks)


if __name__ == '__main__':
    rank_lakes()