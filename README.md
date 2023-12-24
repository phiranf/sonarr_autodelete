# sonarr_autodelete

## About
Simple script, which deletes series after a certain amount of days

## Running this script

### On host
1. Clone this repo and cd into the cloned dir
2. Run ```pip3 install pyarr python-dotenv```
2. Create a ```.env``` file in the same dir with ```sonarr_autodelete.py```
3. Add the following envs to ```.env```
    ```
    SONARR_APIKEY=
    SONARR_HOST=
    ```
4. Add your API Key and Hostname or IP (Hostname and IP have to http:// or https:// before)
5. Run this script with
    ```
    python3 sonarr_autodelete.py --keeptime 30
    ```
## Arguments
```--keeptime```

The keeptime arguments only expects full days and defaults to 30 days and is optional. 

\
```--deleteunavailablemovies```

<sub>(untested after fork)</sup> Without this flag shows will only be removed if the show has been downloaded 30 days before run. If this flag is set shows will be deleted if they are older than 30 days and have not been downloaded yet. This flag is meant for clean up in cases where a show can't be found within an expected time frame and quality.

\
```--dryrun```

Dry run. Show what would be deleted, but don't.

\
```--verbose```

Set this flag for a more detailed output.
