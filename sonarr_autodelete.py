import os
from argparse import ArgumentParser
from datetime import datetime
from tabnanny import verbose
from dotenv import load_dotenv
from pyarr import SonarrAPI

def should_available_serie_delete(serie, currentTime):
    added = serie['added'] # When serie has been downloaded
    return validate_timespan_for_delete(added, currentTime)

def should_unavailable_serie_delete(serie, currentTime):
    added = serie['added']
    return validate_timespan_for_delete(added, currentTime)

def validate_timespan_for_delete(added, currentTime):
    unifiedAdded = added.split('T', 1)[0] # Formatting of date
    dateAddedToDatetime = datetime.strptime(unifiedAdded, '%Y-%m-%d') # More Formatting of date
    dateAddedInSeconds = int(dateAddedToDatetime.timestamp())
    savedTime = currentTime - dateAddedInSeconds # Seconds since download
    if savedTime >= keepTime: return True # Checks if serie has been longer saved than wanted
    else: return False

def daysToSeconds(numberOfDays): # Function Converts Days To Seconds
    days = int(numberOfDays)
    return days * 24 * 60 * 60

load_dotenv()

parser = ArgumentParser()
parser.add_argument('--keeptime', help='Time To Keep series In Days', default=30)
parser.add_argument('--deleteunavailableseries', help='Deletes series From Sonarr, which could not be downloaded within wanted time frame', action='store_true')
parser.add_argument('--dryrun', help='Use this to see what results would look like, without loosing data', action='store_true')
parser.add_argument('--verbose', help='Outputs series deleted', action='store_true')
args = parser.parse_args()

host_url = os.getenv('SONARR_HOST')
api_key = os.getenv('SONARR_APIKEY')

sonarr = SonarrAPI(host_url, api_key)
series = sonarr.get_series()

dt = datetime.today()
secondsNow = int(dt.timestamp()) # Now In Seconds
keepTime = daysToSeconds(int(args.keeptime)) # Time To Keep series before Deleting
dryrun = bool(args.dryrun)
verbose = bool(args.verbose)
deleteunavailableseries = bool(args.deleteunavailableseries)

print('#### ' + dt.strftime("%m/%d/%Y, %H:%M:%S") + ' ####')

if dryrun: print('----THIS IS A DRYRUN----')

print('----SONARR_AUTODELETE----')
print('KEEPTIME: ' + str(args.keeptime))

for serie in series:
        deletable = should_serie_delete(serie, secondsNow)
        if deletable:
            if (dryrun | verbose) | (dryrun & verbose): print('Deleting ' + serie['title'])
            if dryrun == False: sonarr.del_series(serie['id'], True)

print('#### FINISHED ###')
