#!/bin/bash
### IP list Sync ##
instance_id="$1"
ami_name="$2-NOW-SEA-DEPLOY"
dec=$ami_name
origin_region="ap-southeast-1"
copy_region="ap-east-1"


echo "created Image instaneid : $instance_id, ami_name : $ami_name "
echo "aws ec2 create-image --instance-id $instance_id --name $ami_name --description $dec"

# create Image
ami_id=`aws ec2 create-image --instance-id $instance_id --name $ami_name --description $dec | jq -r '.ImageId'`
echo "$ami_name" > /home/ec2-user/shell/created_ami
echo "$ami_id" >> /home/ec2-user/shell/created_ami

# Name taging
key_tag=`aws ec2 create-tags --resources $ami_id --tags Key=Name,Value=$ami_name`

echo "Image Name : $ami_name"
echo "createm Image ID : $ami_id"

if [ -z $ami_id ];
then
echo "END IF NOW IMAGE"

else
  count=0
  while :
  do
      ami_state=`aws ec2 describe-images --image-ids $ami_id | jq -r ".Images | .[0] | .State"`
      sleep 1m
      count=$((count+1))
      echo "count : $count"
      if [ $count -eq 10 ]; then
         echo "IMAGE CREATE FAIL"
         exit 1
      fi
      
      if [ $ami_state = 'available' ]; then
	echo "aws ec2 copy-image --region $copy_region --name $ami_name --source-region $origin_region --source-image-id $ami_id --description $dec"

	# HK copy Image
	hk_ami_id=`aws ec2 copy-image --region $copy_region --name $ami_name --source-region $origin_region --source-image-id $ami_id --description $dec  | jq -r '.ImageId'`
	hk_key_tag=`aws ec2 create-tags --region $copy_region --resources $hk_ami_id --tags Key=Name,Value=$ami_name`
	
	if [ -z $hk_ami_id ]; then
	  echo "HK IMAGE COPY FAIL"
	  exit 1
	else
	  echo "$hk_ami_id" >> /home/ec2-user/shell/created_ami
          echo "END IF SUCCESS"
          break
	fi
      fi
 done
fi
