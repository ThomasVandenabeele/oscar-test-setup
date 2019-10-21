#!/usr/bin/env bash

FILES=./*.xls

SUFFIX=xls

for f in $FILES ; do
	outName=${f%$SUFFIX}
	outName=${outName}csv
	echo $outName
	ssconvert $f $outName

	mv $f ./xls/$f
	
done
