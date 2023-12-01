#bin/sh

module=$1;
replicas=$2;

updateflag=$4;

setime="2023-11-09T11:00:00+00:00";
array=("eks-STG-RCS-EKS-v1_26-NODE-MAIN-70c57a02-9071-be22-3fec-9f4e0b995808" "eks-STG-RCS-EKS-v1_26-NODE-SUB-62c57a03-afd2-96fa-7bec-06d95a8785d2");

for moname in "${array[@]}";
do
  echo $moname
  listSA=`aws autoscaling describe-scheduled-actions --scheduled-action-names "AUTO-ShutDown" --auto-scaling-group-name $moname`

  echo "$listSA";
done

#listSA=`aws autoscaling describe-scheduled-actions --scheduled-action-names AUTO-ShutDown --auto-scaling-group-name $module`

#echo "$listSA";