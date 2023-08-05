# -* coding: utf-8 *-
"""
:py:mod:`swapietl.cli`
======================
Interactive (REPL) command line interface for Star Wars API ETL.
"""
# System imports
import logging
import sys
import os

# Third-party imports
import coloredlogs
from vulcano.app import VulcanoApp

# Local imports
from . import swapi_impl


LOGGER = logging.getLogger('swapietl')
APP = VulcanoApp('swapietl')


@APP.command
def get_top_characters(top=10):
    """Retrieve the results by using swapi-python library

    :param int top: Number of characters to retrieve
    """
    LOGGER.info('Executing the swapi implementation... this may take a minute')
    top_characters = swapi_impl.get_top_character_appearances(top)
    APP.context['swapi_results'] = top_characters


@APP.command
def sort_by(attribute='height', reverse=True):
    """Sort previous results by an attribute

    :param str attribute: Attribute to sort by
    :param bool reverse: Determine sort direction
    """
    if 'swapi_results' not in APP.context:
        LOGGER.error('There are no results to sort.'
                     'Try executing the `get_top_characters` command first')
        return
    LOGGER.info('Sorting by %s', attribute)
    special_sort_field = '_sort_{}'.format(attribute)
    APP.context['swapi_results'] = sorted(
        APP.context['swapi_results'],
        # Can't sort by height without casting it to integer (there are unknowns)
        key=lambda x: getattr(x, special_sort_field) if hasattr(x, special_sort_field) else getattr(x, attribute),
        reverse=reverse
    )


@APP.command
def export_to_csv(filename='~/results.csv'):
    """Export results to a csv file

    :param str filename: Filename where the results will be saved
    """
    if 'swapi_results' not in APP.context:
        LOGGER.error(
            'There are no results to export from swapi implementation.'
            'You may want to execute the command `get_top_characters` before.`'
        )
        return
    if not filename:
        raise FileNotFoundError('You must specify a filename where to save the results')
    filename = os.path.expanduser(filename)
    LOGGER.info('Exporting data to a csv file: %s', filename)
    swapi_impl.export_to_csv(APP.context['swapi_results'], filename)
    LOGGER.info('Export completed.')


@APP.command
def upload_file_to(filename='~/results.csv', url='http://httpbin.org/post'):
    """Upload a file using requests

    :param str filename: File to upload
    :param str url: Url to upload the file
    """
    LOGGER.info('Uploading file')
    filename = os.path.expanduser(filename)
    status_code, text = swapi_impl.upload_file_to(filename, url)
    if status_code == 200:
        LOGGER.info('[%s] File %s uploaded corrrectly', status_code, filename)
    else:
        LOGGER.error('[%s] Unable to upload file to %s', status_code, filename)
    LOGGER.debug('Response from %s: - %s', url, text)


@APP.command
def execute_exercise():
    get_top_characters(top=10)
    sort_by(attribute='height', reverse=True)
    export_to_csv()  # Let defaults here
    upload_file_to()  # Let defaults here


def _prepare_logging():
    format = '[%(asctime)s,%(msecs)03d] %(name)s %(levelname)s %(message)s'
    level = logging.INFO
    # Check and remove verbose mode to not interfere in application execution
    if '-v' in sys.argv:
        level = logging.DEBUG
        sys.argv.pop(sys.argv.index('-v'))
    coloredlogs.install(level=level, fmt=format, logger=LOGGER)


def main():
    _prepare_logging()
    LOGGER.debug('Starting application')
    APP.run()


if __name__ == '__main__':
    main()
