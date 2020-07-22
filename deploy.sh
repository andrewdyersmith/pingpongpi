#!/bin/bash
. "$(dirname "$0")"/credentials

rsync -avzh ./{assets,daemon,web} pi@$HOSTNAME:/home/pi/pingpongpi/

