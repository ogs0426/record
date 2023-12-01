#!/bin/bash
### IP list Sync ##
#
#

count=0
redis_key_patten="$1"
host="stg-rcs-relay-redis1.znvxkf.clustercfg.apn2.cache.amazonaws.com"

if [ $# == 0 ] || [ $# -gt 1 ]
then
    echo "Usage : ./Del_Redis_allKeys.sh <keys_patten>"
    echo "Redis_Host : $host"
    echo "Example :"
    echo "        ./Del_Redis_allKeys.sh \"Test_Key_List_*\""
    exit
fi

echo "Delete start Patten : $redis_key_patten"

listkey=`redis-cli -h $host KEYS $redis_key_patten | awk '{ print }'`

echo $listkey

for akey in $listkey
do
        echo "$akey"

        delresult=`redis-cli -h stg-rcs-relay-redis1.znvxkf.clustercfg.apn2.cache.amazonaws.com DEL $akey`

        echo "delete $akey result= $delresult"

        count=$(($count+1))
done

echo "Delete List $redis_key_patten Count : $count"