__author__ = 'thauser'
from argh import arg
from six import iteritems

import logging
from pnc_cli import swagger_client
from pnc_cli import utils
import pnc_cli.cli_types as types
from pnc_cli.pnc_api import pnc_api


@arg("-p", "--page-size", help="Limit the amount of builds returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_builds(page_size=200, page_index=0, sort="", q=""):
    """
    List all builds
    :param page_size: number of builds returned per query
    :param sort: RSQL sorting query
    :param q: RSQL query
    :return:
    """
    response = utils.checked_api_call(pnc_api.builds_running, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content


@arg("id", help="Running BuildRecord ID to cancel.", type=types.existing_running_build)
def cancel_running_build(id):
    """
    Cancel running build with ID
    """
    data = cancel_running_build_raw(id)
    if data:
        return utils.format_json(data)

def cancel_running_build_raw(id):
    response = utils.checked_api_call(pnc_api.builds_running, 'cancel', id=id)
    if response:
        return response.content