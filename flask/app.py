from flask import Flask, request
from flask.templating import render_template
import boto3
import subprocess

app = Flask(__name__)

ec2 = boto3.client('ec2')

@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')

@app.route('/kube-system')
def kube_system():
    try:
        result = subprocess.run(
            ['kubectl', 'get', 'pod', '-n', 'kube-system', '--field-selector=status.phase==Running', '-o', 'custom-columns=NAME:.metadata.name,STATUS:.status.phase'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        lines = result.stdout.strip().split('\n')
        headers = lines[0].split()
        rows = [line.split() for line in lines[1:]]

    except subprocess.CalledProcessError as e:
        headers = ['Error']
        rows = [[e.stderr]]

    return render_template('kube-system.html', headers=headers, rows=rows)

@app.route('/launch-ec2', methods=['GET', 'POST'])
def launch_ec2():
    if request.method == 'POST':
        subnet_id = request.form['subnet_id']
        ami_id = request.form['ami_id']
        
        try:
            instance = ec2.run_instances(
                ImageId=ami_id,
                InstanceType='t2.micro',
                SubnetId=subnet_id,
                MinCount=1,
                MaxCount=1
            )
            instance_id = instance['Instances'][0]['InstanceId']
            message = f"EC2 instance {instance_id} created successfully!"
        
        except Exception as e:
            message = str(e)
        
        return render_template('launch-ec2.html', message=message)
    
    return render_template('launch-ec2.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)