#!/bin/bash

OUTDIR=$1

cd $OUTDIR

for f in *.svg ; do
	dbus-run-session inkscape $f -D --export-margin=2px --export-pdf=$f.pdf &
done

wait

pdfunite *.svg.pdf cards.pdf
