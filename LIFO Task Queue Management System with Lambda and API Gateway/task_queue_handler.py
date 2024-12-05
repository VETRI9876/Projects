import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('task_queue')

def add_task(event, context):
    timestamp = int(time.time() * 1000)
    table.put_item(
        Item={
            'partition_key': 'tasks',
            'sort_key': timestamp,
            # Add other task details here
        }
    )
    return {
        'statusCode': 200,
        'body': 'Task added successfully'
    }

def process_task(event, context):
    response = table.query(
        KeyConditionExpression='partition_key = :pk',
        ExpressionAttributeValues={
            ':pk': 'tasks'
        },
        ScanIndexForward=False  # Reverse order
    )
    if response['Items']:
        task = response['Items'][0]
        # Process the task here
        table.delete_item(
            Key={
                'partition_key': 'tasks',
                'sort_key': task['sort_key']
            }
        )
        return {
            'statusCode': 200,
            'body': 'Task processed successfully'
        }
    else:
        return {
            'statusCode': 404,
            'body': 'No tasks to process'
        }
