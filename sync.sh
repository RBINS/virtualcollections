#!/usr/bin/env bash
cd $(dirname $0)
echo sure;read
rsync -av ../virtualcollections/ ./\
    --exclude=var/filestorage/ --exclude=*backup*\
    --exclude=*old* --exclude=.installed.cfg --exclude=.mr.developer.cfg
# vim:set et sts=4 ts=4 tw=80:
