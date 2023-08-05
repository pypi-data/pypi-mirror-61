import os
import logging
import argparse
from . import S3Tar

logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s',
)

logging.getLogger('s3_tar.s3_tar').setLevel(
    os.getenv('S3_TAR_LOG_LEVEL', 'INFO').upper()
)


def cli():
    parser = argparse.ArgumentParser(
        description='Tar (and compress) files in s3'
    )
    parser.add_argument(
        "--source-bucket",
        help="base bucket to use",
        required=True,
    )
    parser.add_argument(
        "--target-bucket",
        help=("Bucket that the tar will be saved to."
              " Only needed if different then source bucket"),
        default=None,
    )
    parser.add_argument(
        "--folder",
        help="folder whose contents should be combined",
        required=True,
    )
    parser.add_argument(
        "--filename",
        help=("Output filename for the tar file."
              "\nExtension: tar, tar.gz, or tar.bz2"),
        required=True,
    )
    parser.add_argument(
        "--min-filesize",
        help=("Use to create multiple files if needed."
              " Min filesize of the tar'd files"
              " in [B,KB,MB,GB,TB]. e.x. 5.2GB"),
        default=None,
    )
    args = parser.parse_args()

    job = S3Tar(
        args.source_bucket,
        args.filename,
        target_bucket=args.target_bucket,
        min_file_size=args.min_filesize,
    )
    job.add_files(args.folder)
    job.tar()
