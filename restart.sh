#! /bin/sh
./bin/supervisorctl restart instance1
sleep 30s
./bin/supervisorctl restart instance2
sleep 30s
./bin/supervisorctl restart instance3
sleep 30s
./bin/supervisorctl restart instance4
