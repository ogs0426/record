#!/bin/bash
### IP list Sync ##

instance_id="$1"
ami_name="$2-$3"
templete_id="$4"
dec=$ami_name

echo "created Image instaneid : $instance_id, ami_name : $ami_name, templete_id : $templete_id "
echo "aws ec2 create-image --instance-id $instance_id --name $ami_name --description $dec"

# create Image
ami_id=`aws ec2 create-image --instance-id $instance_id --name $ami_name --description $dec | jq -r '.ImageId'`

# Name taging
key_tag=`aws ec2 create-tags --resources $ami_id --tags Key=Name,Value=$ami_name`

#ami_id='ami-0aa62b5484e1228a6'

echo "Image Name : $ami_name"
echo "createm Image ID : $ami_id"

if [ -z $ami_id ];
then

echo "END IF NOW IMAGE"

else

# lasted Version
la_version=`aws ec2 describe-launch-template-versions --launch-template-id $templete_id | jq -r ".LaunchTemplateVersions | .[0] | .VersionNumber"`

echo "last version $la_version"

aws ec2 create-launch-template-version --launch-template-id $templete_id --source-version $la_version --version-description $dec --launch-template-data "{\"ImageId\":\"$ami_id\"}"

echo "END IF SUCCESS"

fi


