from subprocess import call
import logging

import click
import git

from dbispipeline.core import Core
from dbispipeline.output_handlers import PostGresOutputHandler, PrintHandler
from dbispipeline.utils import LOGGER
from dbispipeline.utils import restore_backup
from dbispipeline.utils import prepare_slurm_job



@click.command(help='Uses the plan file specified in PLAN to run the dbis '
    'pipeline.')
@click.option('--dryrun', is_flag=True, help='Don\'t store results into DB')
@click.option('--force', is_flag=True, help='Run even if git is dirty')
@click.option('-v', '--verbose', is_flag=True, help='increase logging')
@click.option('--slurm', is_flag=True, help='create slurm file and submit')
@click.option('--restore', type=str, help='result file to be restored')
@click.option(
    '--mail', type=click.Choice(['none', 'run', 'total']), default='none',
    help='Mail notification level. Choose one of [None, \'run\', \'total\''
    ']. If set no None, no mails will be sent. if set to \'run\', one info'
    ' mail will be sent for each run. If set to \'total\', one mail will '
    'be sent after the entire pipeline is complete.')
@click.argument('plan', type=click.Path(exists=True))
def _main(dryrun, force, verbose, slurm, restore, mail, plan):
    main(dryrun, force, verbose, slurm, restore, mail, plan)


# this method is split to allow the legacy method of invoking via the modules'
# __main__.py file to re-use this code.
def main(dryrun, force, verbose, slurm, restore, mail, plan):
    """Entry point that executes the pipeline given a configuration."""

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.debug('setting logging level to DEBUG')

    if args.restore:
        restore_backup(args.restore, [PrintHandler(), PostGresOutputHandler()])
        exit(0)

    if not args.force:
        try:
            repo = git.Repo(search_parent_directories=True)
            if repo.is_dirty():
                LOGGER.error(
                    "Please commit your changes before you run the pileline.")
                exit(1)
        except git.GitError:
            pass

    if args.slurm:
        jobfile = prepare_slurm_job(args)
        call(['sbatch', jobfile])
    else:
        Core(
            args.configurationfile,
            dryrun=args.dryrun,
            mail=args.mail).run()
