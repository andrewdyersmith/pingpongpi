#!/bin/bash
. "$(dirname "$0")"/credentials

rsync -avzh ./{daemon,web} pi@$HOSTNAME:/home/pi/pingpongpi/

