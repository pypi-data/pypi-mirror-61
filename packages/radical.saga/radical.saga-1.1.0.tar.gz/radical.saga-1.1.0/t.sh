#!/bin/sh

state=DONE

if test "$state" != "DONE" -a "$state" != "FAILED" -a "$state" != "CANCELED"
then
    echo "job FOO in incorrect state ($state != DONE|FAILED|CANCELED)"
else
    echo ok
fi
