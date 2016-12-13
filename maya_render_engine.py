import os
import boto3
from tempfile import TemporaryFile
from bpc_serverless import MayaEngine

def render_handler( event=None, context=None ):
    if context is None: context = {'Error': 'no context data'}
    if event is None:   event   = {'Error': 'no event data'}

    bucket = 'bpc-serverless'
    path = event['path'] if 'path' in event else 'test/no_event_path'
    key = '/'.join( ( 'pages', path, 'index.html' ) )

    # Construct payload and render page markup
    source = MayaEngine.render(
        payload={
            'event': event,
            'context': context,
            'environ': os.environ,
            'word': 'AWS Lambda'
        }
    )

    # Write page markup to AWS S3
    aws_s3 = boto3.client('s3')
    tmp_file = TemporaryFile()

    try:
        tmp_file.write(source)
        aws_s3.upload_fileobj( tmp_file, bucket, key, ExtraArgs={'ContentType': "text/html", 'ACL': "public-read"} )
    finally:
        tmp_file.close()

    return 'rendered: ' + '/'.join( ( bucket, key ) )
