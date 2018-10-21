import pytz
import boto3

# Delete 30 day old server backups from DigitalOcean Spaces bucket
# Initialize a session using Spaces
session = boto3.session.Session()
do_client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id='abc',
                        aws_secret_access_key='xyz')
d = datetime.today() - timedelta(days=30)
utc = pytz.UTC
d = utc.localize(d)
response = do_client.list_objects(Bucket='locklin-networks')
for row in response["Contents"]:
    d2 = row["LastModified"]
    if d2 < d:
        print "time to delete " + str(row["Key"]) + " / " + str(row["LastModified"])
        # Delete object
        response = do_client.delete_object(Bucket='locklin-networks', Key=row["Key"])
        print response
