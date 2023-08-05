"""Communication with GraceDB."""
from http.client import HTTPException
import functools
from socket import gaierror
import re

from ligo.gracedb import rest
from celery.utils.log import get_task_logger

from ..import app
from ..util import PromiseProxy

client = PromiseProxy(rest.GraceDb,
                      ('https://' + app.conf.gracedb_host + '/api/',),
                      {'fail_if_noauth': True, 'reload_certificate': True})

log = get_task_logger(__name__)


class RetryableHTTPError(rest.HTTPError):
    """Exception class for server-side HTTP errors that we should retry."""


def catch_retryable_http_errors(f):
    """Decorator to capture server-side errors that we should retry.

    We retry HTTP status 502 (Bad Gateway), 503 (Service Unavailable), and
    504 (Gateway Timeout).
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except rest.HTTPError as e:
            if e.status in {429, 502, 503, 504}:
                raise RetryableHTTPError(e.status, e.reason, e.message)
            else:
                raise

    return wrapper


def task(*args, **kwargs):
    return app.task(*args, **kwargs,
                    autoretry_for=(gaierror, RetryableHTTPError,
                                   TimeoutError, HTTPException),
                    default_retry_delay=20.0, retry_backoff=True,
                    retry_kwargs=dict(max_retries=10))


versioned_filename_regex = re.compile(
    r'^(?P<filename>.*?)(?:,(?P<file_version>\d+))?$')


def _parse_versioned_filename(versioned_filename):
    match = versioned_filename_regex.fullmatch(versioned_filename)
    filename = match['filename']
    file_version = match['file_version']
    if file_version is not None:
        file_version = int(file_version)
    return filename, file_version


@task(shared=False)
@catch_retryable_http_errors
def create_event(filecontents, search, pipeline, group):
    """Create an event in GraceDB."""
    response = client.createEvent(group=group, pipeline=pipeline,
                                  filename='initial.data', search=search,
                                  filecontents=filecontents)
    return response.json()['graceid']


@task(ignore_result=True, shared=False)
@catch_retryable_http_errors
def create_label(label, graceid):
    """Create a label in GraceDB."""
    try:
        with client.writeLabel(graceid, label):
            pass  # Close without reading response; we only needed the status
    except rest.HTTPError as e:
        # If we got a 400 error because no change was made, then ignore
        # the exception and return successfully to preserve idempotency.
        messages = {
            '"The \'ADVREQ\' label cannot be applied to request a signoff '
            'because a related signoff already exists."',

            '"The fields superevent, label must make a unique set."'
        }
        if e.message not in messages:
            raise


@task(ignore_result=True, shared=False)
@catch_retryable_http_errors
def remove_label(label, graceid):
    """Create a label in GraceDB."""
    try:
        with client.removeLabel(graceid, label):
            pass  # Close without reading response; we only needed the status
    except rest.HTTPError as e:
        # If the label did not exist, then GraceDB will return a 404 error.
        # Don't treat this as a failure because we got what we wanted: for the
        # label to be removed.
        if e.status != 404:
            raise


@task(ignore_result=True, shared=False)
@catch_retryable_http_errors
def create_signoff(status, comment, signoff_type, graceid):
    """Create a label in GraceDB."""
    with client.create_signoff(graceid, signoff_type, status, comment):
        pass  # Close without reading response; we only needed the status


@task(ignore_result=True, shared=False)
@catch_retryable_http_errors
def create_tag(filename, tag, graceid):
    """Create a tag in GraceDB."""
    filename, file_version = _parse_versioned_filename(filename)
    log = get_log(graceid)
    if file_version is None:
        *_, entry = (e for e in log if e['filename'] == filename)
    else:
        *_, entry = (e for e in log if e['filename'] == filename
                     and e['file_version'] == file_version)
    log_number = entry['N']
    try:
        with client.addTag(graceid, log_number, tag):
            pass  # Close without reading response; we only needed the status
    except rest.HTTPError as e:
        # If we got a 400 error because no change was made, then ignore
        # the exception and return successfully to preserve idempotency.
        if e.message != '"Tag is already applied to this log message"':
            raise


@task(shared=False)
@catch_retryable_http_errors
def create_voevent(graceid, voevent_type, **kwargs):
    """Create a VOEvent.

    Returns
    -------
    str
        The filename of the new VOEvent.

    """
    response = client.createVOEvent(graceid, voevent_type, **kwargs).json()
    return response['filename']


@task(shared=False)
@catch_retryable_http_errors
def download(filename, graceid):
    """Download a file from GraceDB."""
    return client.files(graceid, filename, raw=True).read()


@task(ignore_result=True, shared=False)
@catch_retryable_http_errors
def expose(graceid):
    """Expose an event to the public.

    Notes
    -----
    If :obj:`~gwcelery.conf.expose_to_public` is False, then this because a
    no-op.

    """
    if app.conf['expose_to_public']:
        with client.modify_permissions(graceid, 'expose'):
            pass  # Close without reading response; we only needed the status


@task(shared=False)
@catch_retryable_http_errors
def get_events(*args, **kwargs):
    """Get events from GraceDB."""
    return list(client.events(*args, **kwargs))


@task(shared=False)
@catch_retryable_http_errors
def get_event(graceid):
    """Retrieve an event from GraceDB."""
    return client.event(graceid).json()


@task(shared=False)
@catch_retryable_http_errors
def get_group(graceid):
    """Retrieve the search field of an event from GraceDB."""
    return client.event(graceid).json()['group']


@task(shared=False)
@catch_retryable_http_errors
def get_search(graceid):
    """Retrieve the search field of an event from GraceDB."""
    return client.event(graceid).json()['search']


@task(shared=False)
@catch_retryable_http_errors
def get_labels(graceid):
    """Get all labels for an event in GraceDB."""
    return {row['name'] for row in client.labels(graceid).json()['labels']}


@task(shared=False)
@catch_retryable_http_errors
def get_log(graceid):
    """Get all log messages for an event in GraceDB."""
    return client.logs(graceid).json()['log']


@task(shared=False)
@catch_retryable_http_errors
def get_superevent(graceid):
    """Retrieve a superevent from GraceDB."""
    return client.superevent(graceid).json()


@task(shared=False)
@catch_retryable_http_errors
def replace_event(graceid, payload):
    """Get an event from GraceDB."""
    with client.replaceEvent(graceid, 'initial.data', filecontents=payload):
        pass  # Close without reading response; we only needed the status


@task(shared=False)
@catch_retryable_http_errors
def upload(filecontents, filename, graceid, message, tags=()):
    """Upload a file to GraceDB."""
    result = client.writeLog(
        graceid, message, filename, filecontents, tags).json()
    return '{},{}'.format(result['filename'], result['file_version'])


@app.task(shared=False)
@catch_retryable_http_errors
def get_superevents(*args, **kwargs):
    """List matching superevents in gracedb.

    Parameters
    ----------
    *args
        arguments passed to :meth:`GraceDb.superevents`
    **kwargs
        keyword arguments passed to :meth:`GraceDb.superevents`

    Returns
    -------
    superevents : list
        The list of the superevents.

    """
    return list(client.superevents(*args, **kwargs))


@task(ignore_result=True, shared=False)
@catch_retryable_http_errors
def update_superevent(superevent_id, t_start=None,
                      t_end=None, t_0=None, preferred_event=None,
                      em_type=None, coinc_far=None):
    """
    Update superevent information. Wrapper around
    :meth:`updateSuperevent`

    Parameters
    ----------
    superevent_id : str
        superevent uid
    t_start : float
        start of superevent time window, unchanged if None
    t_end : float
        end of superevent time window, unchanged if None
    t_0 : float
        superevent t_0, unchanged if None
    preferred_event : str
        uid of the preferred event, unchanged if None

    """
    try:
        with client.updateSuperevent(superevent_id,
                                     t_start=t_start, t_end=t_end, t_0=t_0,
                                     preferred_event=preferred_event,
                                     em_type=em_type, coinc_far=coinc_far):
            pass  # Close without reading response; we only needed the status
    except rest.HTTPError as e:
        # If we got a 400 error because no change was made, then ignore
        # the exception and return successfully to preserve idempotency.
        error_msg = '"Request would not modify the superevent"'
        if not (e.status == 400 and e.message == error_msg):
            raise


@task(shared=False)
@catch_retryable_http_errors
def create_superevent(graceid, t0, t_start, t_end, category):
    """Create new superevent in GraceDB with `graceid`

    Parameters
    ----------
    graceid : str
        graceid with which superevent is created.
    t0 : float
        ``t_0`` parameter of superevent
    t_start : float
        ``t_start`` parameter of superevent
    t_end : float
        ``t_end`` parameter of superevent
    category : str
        superevent category

    """
    try:
        response = client.createSuperevent(t_start, t0, t_end,
                                           preferred_event=graceid,
                                           category=category)
        return response.json()['superevent_id']
    except rest.HTTPError as e:
        error_msg = 'is already assigned to a Superevent'
        if not (e.status == 400 and error_msg in e.message):
            raise


@task(ignore_result=True, shared=False)
@catch_retryable_http_errors
def add_event_to_superevent(superevent_id, graceid):
    """Add an event to a superevent in GraceDB."""
    try:
        with client.addEventToSuperevent(superevent_id, graceid):
            pass  # Close without reading response; we only needed the status
    except rest.HTTPError as e:
        error_msg = 'is already assigned to a Superevent'
        if not (e.status == 400 and error_msg in e.message):
            raise
