"""
    This file is deleting the files that have delete_marker tags on S3 recusively go in all the folders and subfolders of that bucket.
"""
import boto3, argparse
import sys

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def exit(message=''):
    sys.exit(message)

# initiate the parser
parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument("--access_key", "-A", help="Access key of s3(Required)", required=True)
requiredNamed.add_argument("--secret_key", "-S", help="Secret key of s3(Required)", required=True)
requiredNamed.add_argument("--bucket", "-B", help="Bucket name of s3(Required)", required=True)
requiredNamed.add_argument("--region", "-R", help="S3 region(Required)", required=True)
parser.add_argument("--folder", "-F", help="Folder of s3 in which all files you want to delete.(optional)", default='/')
parser.add_argument("--delete", "-D", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Confirm if you want to delete(Default False).(optional)")



# read arguments from the command line
args = parser.parse_args()

# Connections with s3
client = boto3.client(
    's3',
    aws_access_key_id=args.access_key,
    aws_secret_access_key=args.secret_key,
)
s3 = boto3.resource(
    's3',
    region_name=args.region,
    aws_access_key_id=args.access_key,
    aws_secret_access_key=args.secret_key,
)

bucket = s3.Bucket(BUCKET_NAME)
def init(Prefix='', Delimiter='/'):
    result = client.list_object_versions(
                                        Bucket=args.bucket,
                                        Prefix=Prefix,
                                        Delimiter='/'
                                        )
    # CommonPrefixes key has all the sub folders in current directory
    common_prefixes = result.get('CommonPrefixes')
    # List of files to be deleted in current folder
    delete_marked_files = result.get('DeleteMarkers')
    if delete_marked_files:
        for delete_marked_file in delete_marked_files:
            print 'Found file >>>'
            print delete_marked_file['Key']
            if args.delete:
                try:
                    response = s3.ObjectVersion(
                    BUCKET_NAME,
                    delete_marked_file['Key'],
                    delete_marked_file['VersionId']
                    )
                    # response.delete()
                except Exception as e:
                    # TODO: Not handeled exception yet
                    print 'Could not delete file>>'
                    print delete_marked_file['Key']
    else:
        print 'No deleted files found in folder>>'
        print Prefix
    if common_prefixes:
        for common_prefix in common_prefixes:
            folder = common_prefix.get('Prefix')
            # Recursively call init function to go into all sub folders
            init(Prefix=folder)

init(Prefix=args.folder)
