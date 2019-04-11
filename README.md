# About this file
(Python) This file is deleting the files that have delete_marker tags on S3 recusively go in all the folders and subfolders of that bucket.
# Requirments
Python2.7
# How To Install
Take pull
Install requirements.txt
Run "python2.7 run.py -h"(This will give you help to let you know the required params to pass)
# Example to run
Run example
# Varialbes to be passed
"-A", help="Access key of s3(Required)"
"-S", help="Secret key of s3(Required)"
"-B", help="Bucket name of s3(Required)"
"-R", help="S3 region(Required)"
"-F", help="Folder of s3 in which all files you want to delete.(optional)"{If not passed it will go into all the folder of that bucket}
"-D", help="Confirm if you want to delete(Default False).(optional)"{If not given it will not delete the files but only print the files that will be deleted.}
"python2.7 s3.py -F resources/ -A XXXXXX -S XXXXXX -R XXXXX -D (Bool y,n) -F XXXXX -B XXXXXX"

