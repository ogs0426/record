#!/bin/bash
template_id=$1
region=$2
ami_name=`sed -n -e '1p' /home/ec2-user/shell/created_ami`
ami_id=`sed -n -e '2p' /home/ec2-user/shell/created_ami`
template_region='ap-southeast-1' # sg

if [ $region = 'hk' ]; then
  ami_id=`sed -n -e '3p' /home/ec2-user/shell/created_ami`
  template_region='ap-east-1' # hk
fi
echo "region : $region, template_region : $template_region"
#lasted Version
la_version=`aws ec2 describe-launch-template-versions --region $template_region --launch-template-id $template_id | jq -r ".LaunchTemplateVersions | .[0] | .VersionNumber"`
echo "$template_id last version : $la_version"
aws ec2 create-launch-template-version --region $template_region --launch-template-id $template_id --source-version $la_version --version-description $ami_name --launch-template-data "{\"ImageId\":\"$ami_id\"}"
 
