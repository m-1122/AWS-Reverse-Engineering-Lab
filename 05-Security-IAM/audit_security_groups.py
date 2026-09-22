import boto3

ec2 = boto3.client('ec2')

def audit_security_groups():
    response = ec2.describe_security_groups()
    for sg in response['SecurityGroups']:
        sg_id = sg['GroupId']
        sg_name = sg['GroupName']
        for rule in sg['IpPermissions']:
            from_port = rule.get('FromPort', -1)
            to_port = rule.get('ToPort', -1)
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    if from_port <= 22 <= to_port or from_port <= 3389 <= to_port or from_port == -1:
                        print(f"[!] ZAGROŻENIE: SG '{sg_name}' ({sg_id}) ma otwarcie na świat na porcie {from_port}-{to_port}!")

if __name__ == "__main__":
    print("Rozpoczynam audyt Security Groups...")
    audit_security_groups()
