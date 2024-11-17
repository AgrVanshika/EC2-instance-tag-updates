import boto3

# Step 1: Connect to AWS EC2
ec2 = boto3.client('ec2')

# Step 2: Fetch all instances
instances = ec2.describe_instances()['{mention column}']

# Required tags dictionary for consistency
required_tags = {'Environment': 'Production', 'Owner': 'Team A'}

for reservation in instances:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        
        # Step 3: Get Current Tags
        current_tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        
        # Step 4: Determine Missing or Incorrect Tags
        tags_to_update = []
        for key, value in required_tags.items():
            if current_tags.get(key) != value:
                tags_to_update.append({'Key': key, 'Value': value})
        
        # Step 5: Update Tags if necessary
        if tags_to_update:
            ec2.create_tags(Resources=[instance_id], Tags=tags_to_update)
            print(f"Updated tags for instance {instance_id}")

# Optional: Step 6: Log changes and verify updates
