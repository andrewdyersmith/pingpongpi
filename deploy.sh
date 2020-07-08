#!/bin/bash
HOST=$1

rsync -avzh ./{daemon,web} pi@$HOST:/home/pi/pingpongpi/

