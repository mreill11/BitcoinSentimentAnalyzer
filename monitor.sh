#!/bin/bash
until ./crawl.py; do
	echo "'crawl.py' crashed with exit code $?. Restarting..." >&2
	sleep 1
done
