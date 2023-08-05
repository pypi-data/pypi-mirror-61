import click
import input_helper as ih
from aws_info_helper import S3, AWS_S3, AWS_S3_LAST_FILE, get_profiles


@click.command()
@click.option(
    '--non-interactive', '-n', 'non_interactive', is_flag=True, default=False,
    help='Do not start an ipython session at the end'
)
@click.option(
    '--all', '-a', 'all', is_flag=True, default=False,
    help='Update info from all profiles found in ~/.aws/credentials'
)
@click.option(
    '--profile', '-p', 'profile', default='default',
    help='Name of AWS profile to use'
)
def main(**kwargs):
    """Update info in AWS_S3 redis-helper collection"""
    if kwargs['all'] is True:
        for profile in get_profiles():
            s3 = S3(profile)
            s3.update_collection()
    else:
        s3 = S3(kwargs['profile'])
        s3.update_collection()
    if kwargs['non_interactive'] is not True:
        ih.start_ipython(s3=AWS_S3, s3_last_file=AWS_S3_LAST_FILE)


if __name__ == '__main__':
    main()
