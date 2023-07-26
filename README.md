# waveshare-citibike-mta
NYC Citibike and MTA Subway Alerts For RPi Zero WH + Waveshare 5.83" E-Ink Display

SNPfTrainChecker.py -- contains the functions that pull the next 5 uptown and downtown train departures from the York St F stop (after ignoring any that come in the next 5 min as the station is 5min away from the location), and writes the latest three to /latestJSONs/arrival_times.json
- The reason I pull 5 is that I was finding that the gfts (a google protocol for publishing train times, like RSS I guess) would sometimes have blank values, so I gave a buffer of two to be safe

SNPCitibikeChecker.py -- contains the functions that pull the number of electric and "classic" citibikes at the two nearest stops from citibike's gbfs (same as gtfs but for bikeshares) and writes the latest information to /latestJSONs/stations.json
/source_files/template_snp-frame.png -- a template that I designed in adobe illustrator, to avoid wasting time and energy creating these graphics each time it writes the script, not to mention that the library I use to write the up-to-date info doesn't render it as well as Illustrator does

SNP_frame-image-generator.py -- this is the main script, which uses the above two scripts as libraries, pulls the functions from them, and does the actual work of creating the JSONs and generates an up-to-date file at /latest_images/{time_str}_snp-frame.png. If for some reason.
To cut down on storing unnecessary files, it deletes all but the latest 5 pngs in the /latest_images folder.

To make it more resilient, if either Request from either the citibikechecker or ftrainchecker functions returns with anything but Status=200, I have it return, instead of the actual numbers, the string "N/A".

SNP-display-latest-frame.py -- this takes the latest file in /latest_images and actually displays it on the waveshare screen. because it's an e-ink display, one only needs to push it to the screen and the image will persist if the program is done (and even if the computer or screen were to be unplugged). 

clear-screen.py -- does what it says on the tin. refreshes the waveshare e-ink screen so that I don't get any burn-in (not likely, as it can take as many as 10 days to cause burn in on an e-ink screen)
