#!/usr/bin/env bash
p="/mars/minitage/zope/virtualcollections"
cd $(dirname $0)
set -x
for i in var/filestorage/Data.fs var/blobstorage/;do 
    rsync -av --delete  $p/$i $i --exclude=*backup* --exclude=*old*
done
./bin/zeoserver restart
