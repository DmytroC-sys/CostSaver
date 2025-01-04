import boto3
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# AWS Credentials from environment variables or AWS IAM roles
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-west-1')  # Default region

# Initialize Boto3 EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, 
                          aws_secret_access_key=aws_secret_key, region_name=aws_region)

# Example cost data for EC2 instances (simplified for demonstration)
EC2_COST_PER_HOUR = {
    't2.micro': 0.0116,  # Example cost per hour in USD
    't2.small': 0.023,
    't3.medium': 0.0376,
}

@app.route('/fetch_instances', methods=['GET'])
def fetch_instances():
    """
    Fetch EC2 instances and their details from AWS.
    """
    try:
        # Fetch EC2 instances
        response = ec2_client.describe_instances()
        instances = []

        # Extract relevant data for each instance
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_data = {
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                }
                instances.append(instance_data)

        return jsonify({'instances': instances}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate_cost', methods=['POST'])
def calculate_cost():
    """
    Calculate the estimated cost of EC2 instances based on type and usage.
    """
    data = request.get_json()
    instance_type = data.get('instance_type')
    hours_used = data.get('hours_used', 1)  # Default to 1 hour if not provided

    if instance_type not in EC2_COST_PER_HOUR:
        return jsonify({'error': f'Unknown instance type: {instance_type}'}), 400

    # Calculate the cost based on the hourly rate and usage
    hourly_rate = EC2_COST_PER_HOUR[instance_type]
    estimated_cost = hourly_rate * hours_used

    return jsonify({
        'instance_type': instance_type,
        'hours_used': hours_used,
        'estimated_cost_usd': round(estimated_cost, 4)
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

