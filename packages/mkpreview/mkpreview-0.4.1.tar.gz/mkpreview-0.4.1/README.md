# CLI Usage


### Command Line Usage


```
usage: mkpreview.py [-h] [--version] [-v] [-dr] [-d] [-q] [-w TILE_WIDTH]
                    [-r TILE_ROWS] [-c TILE_COLS] [-b TILE_BK_COLOR]
                    [-p TILE_FG_COLOR] [-i IN_FILE] [-o OUT_DIR] [-m]
                    [-s DBFILE] [-create-new-db] [-override OVERRIDE]
                    [-colors] [-studio-id STUDIO_ID] [-part-id PART_ID]
                    [-hwaccel {cuda,videotoolbox}]

This program will create a video preview file of a given video

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         Turn on verbose output
  -dr, --dryrun         Dryrun enabled no changes will occur
  -d, --debug           Turn on Debugging Mode
  -q, --quiet           No output is produced
  -w TILE_WIDTH, --tile-width TILE_WIDTH
                        Tile width - Tiles are sqaure
  -r TILE_ROWS, --tile-rows TILE_ROWS
                        Number of rows for a preview
  -c TILE_COLS, --tile-cols TILE_COLS
                        Number of columns for a preview
  -b TILE_BK_COLOR, --tile-backgrond TILE_BK_COLOR
                        Tile Background Color
  -p TILE_FG_COLOR, --tile-foreground TILE_FG_COLOR
                        Tile Pen Color
  -fs FONT_SIZE, --font-size FONT_SIZE
                        Font size for text default is 24pt
  -i IN_FILE, --input IN_FILE
                        Video input, can by a file or directory. If directory,
                        it will not be recursive
  -o OUT_DIR, --output-dir OUT_DIR
                        Where to put the finished files
  -m, --md5             Add the MD5 of the file to the filename
  -s DBFILE, --store-db-file DBFILE
                        Store the video information in SQLI3te file
  -create-new-db        Create a new database file
  -override OVERRIDE    save image with this filename override all other
                        possible choices
  -colors               Display List of Available Colors
  -studio-id STUDIO_ID  Replace the this id, first part of filename for a
                        part-id use in conjunction with -part-id
  -part-id PART_ID      Change first alpha part of filename for the part-id
  -hwaccel {cuda,videotoolbox}
                        Enable Hardware acceleration for videotoolbox or cuda

The filename of the output will be the part_id-md5-originalBaseName.png. If
the part_id and md5 are unset the filename will be the original base name.png

Environment Variables:
----------------------
MKP_DEBUG - Debugging on/off
MKP_TILE_WIDTH
MKP_TILE_ROWS
MKP_TILE_COLS
MKP_TILE_BK_COLOR
MKP_TILE_FG_COLOR
MKP_IN_FILE
MKP_OUT_DIR
MKP_MD5
MKP_DBFILE
MKP_CREATEDB
```

### Example 1:
[sample](http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4)



```
./mkpreview.py -i /Users/colinbitterfield/Downloads/WhatCarCanYouGetForAGrand.mp4 \
  	--output-dir /tmp/ --md5 --tile-width 320 --tile-rows 7 \
 	--tile-cols 7 --tile-background yellow \
 	--tile-foreground blue --font-size 60 \
 	--store-db-file /tmp/myDatabase.db \
 	-create-new-db -override previewcard
```


### Results

<IMG src="https://github.com/Studio-51/mkpreview/blob/master/docs/images/previewcard.jpg">
