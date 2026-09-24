#!/usr/bin/env python3
"""
AWS Multi-Tool Auditor (SAA-C03 Lab)
- Audytuje reguły Security Groups pod kątem otwartych portów (0.0.0.0/0).
- Audytuje kubełki S3 pod kątem optymalizacji kosztów (Versioning & Lifecycle).
Uruchomienie z roota: python3 aws_auditor.py
"""

import boto3
from botocore.exceptions import ClientError

def audit_security_groups():
    print("\n[*] --- AUDYT SECURITY GROUPS (Bezpieczeństwo) ---")
    ec2 = boto3.client('ec2')
    
    try:
        response = ec2.describe_security_groups()
    except ClientError as e:
        print(f"[-] Błąd AWS EC2: {e}")
        return

    print(f"{'GROUP ID':<15} | {'GROUP NAME':<25} | {'PORT':<6} | {'CIDR'}")
    print("-" * 65)

    for sg in response.get('SecurityGroups', []):
        sg_id = sg['GroupId']
        sg_name = sg['GroupName']
        
        for perm in sg.get('IpPermissions', []):
            from_port = perm.get('FromPort', 'All')
            to_port = perm.get('ToPort', 'All')
            
            for ip_range in perm.get('IpRanges', []):
                cidr = ip_range.get('CidrIp')
                if cidr == '0.0.0.0/0':
                    port_str = f"{from_port}" if from_port == to_port else f"{from_port}-{to_port}"
                    print(f"{sg_id:<15} | {sg_name:<25} | {port_str:<6} | {cidr} [UWAGA: Otwarte na świat!]")

def audit_s3_buckets():
    print("\n[*] --- AUDYT KUBEŁKÓW S3 (Koszty i Wersjonowanie) ---")
    s3 = boto3.client('s3')
    
    try:
        response = s3.list_buckets()
    except ClientError as e:
        print(f"[-] Błąd AWS S3: {e}")
        return

    print(f"{'NAZWA KUBEŁKA':<30} | {'REGION':<12} | {'WERSJONOWANIE':<12} | {'LIFECYCLE'}")
    print("-" * 75)

    for bucket in response.get('Buckets', []):
        name = bucket['Name']
        
        try:
            loc = s3.get_bucket_location(Bucket=name)
            region = loc.get('LocationConstraint') or 'us-east-1'
        except ClientError:
            region = 'Unknown'

        versioning = "Disabled"
        try:
            ver = s3.get_bucket_versioning(Bucket=name)
            if ver.get('Status') == 'Enabled':
                versioning = "Enabled"
        except ClientError:
            versioning = "No Access"

        lifecycle = "Brak"
        try:
            s3.get_bucket_lifecycle_configuration(Bucket=name)
            lifecycle = "Aktywny"
        except ClientError:
            lifecycle = "Brak"

        print(f"{name:<30} | {region:<12} | {versioning:<12} | {lifecycle}")

if __name__ == "__main__":
    print("[+] Uruchamiam uniwersalny audytor infrastruktury AWS...")
    audit_security_groups()
    audit_s3_buckets()
    print("\n[+] Audyt zakończony pomyślnie.")
