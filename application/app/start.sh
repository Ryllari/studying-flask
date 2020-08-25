#!/bin/sh

wait-for db:5432

cd /usr/src/app && flask db upgrade head && flask run -h 0.0.0.0
