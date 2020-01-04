import boto3

s3 = boto3.client('s3')
bucket_name = 'ece1779-assign2'
bucket_url = 'https://s3.amazonaws.com/ece1779-assign2/'


def clear_s3():
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        print(key['Key'])
        s3.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': [
                    {
                        'Key': key['Key'],
                        # 'VersionId': 'string'
                    },
                ],
                'Quiet': True
            },
            # MFA='string',
            # RequestPayer='requester',
            # BypassGovernanceRetention=True | False
        )


def upload_file(dirname, filename):
    s3.upload_file(dirname + '/' + filename, bucket_name, filename)
    return bucket_url + filename
