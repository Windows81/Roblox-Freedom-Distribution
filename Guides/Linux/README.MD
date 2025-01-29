To launch Freedom Distribution, your command line will look something like this:

```
./RFD player -h 127.0.0.1 -p 2005
```

Make sure you have wine and an initialized wine prefix for this to work properly.

To create a new wine prefix you can just do

```
export WINEPREFIX=<directorywhereyouwantthewineprefix to be stored.>
wineboot --init
```

If you want to specify the wineprefix if it is defaulting on ~/.wine while running the RFD command, then you can do:
```
WINEPREFIX=<wine prefix directory> ./RFD player -h <ip> -p <port>
```