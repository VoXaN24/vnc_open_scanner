# vnc_open_scanner
An python script for scanning open vnc server


## How to use ?
You must have a file that follows the following nomenclature:

```
ip,port1-port2...endport
```

If you do not put any port, the script takes port 5900 by default

```
pip3 install -r requierement.txt

python3 vnc_open_scanner.py
```

## The Screeshot fonction work in cli only ?

YES! It use an Virtal X server for it !

## Where the result is ?
All the screen are in the "screen" folder, the sucess IP is in sucess.txt and failed IP in failed.txt

### This is for Educationnal purpose only !
