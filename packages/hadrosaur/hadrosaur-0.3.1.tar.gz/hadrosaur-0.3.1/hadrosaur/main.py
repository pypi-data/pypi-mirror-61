import time
import traceback
import json
import os
import logging

_START_FILENAME = 'start_time'
_END_FILENAME = 'end_time'
_STATUS_FILENAME = 'status'
_ERR_FILENAME = 'error.log'
_RESULT_FILENAME = 'result.json'
_STORAGE_DIRNAME = 'storage'
_LOG_FILENAME = 'run.log'

# TODO log colors


class Project:

    def __init__(self, basepath):
        if os.path.exists(basepath) and not os.path.isdir(basepath):
            raise RuntimeError(f"Project base path is not a directory: {basepath}")
        os.makedirs(basepath, exist_ok=True)
        self.basedir = basepath
        self.collections = {}  # type: dict
        self.logger = logging.getLogger(basepath)

    def resource(self, name):
        """
        Define a new resource by name and function
        """
        if name in self.collections:
            raise RuntimeError(f"Resource name has already been used: '{name}'")
        res_path = os.path.join(self.basedir, name)
        os.makedirs(res_path, exist_ok=True)

        def wrapper(func):
            self.collections[name] = {'func': func, 'dir': res_path}
            return func
        return wrapper

    def status(self, coll_name=None, resource_id=None):
        """
        Fetch some aggregated statistics about a collection.
        """
        if coll_name and resource_id:
            return self._resource_status(coll_name, resource_id)
        elif coll_name:
            return self._coll_status(coll_name)
        else:
            raise TypeError("Pass in a collection name or both a collection name and resource ID.")

    def _validate_coll_name(self, coll_name):
        """
        Make sure the collection exists for this project.
        """
        if coll_name not in self.collections:
            raise RuntimeError(f"Unknown collection '{coll_name}'")
        coll_path = os.path.join(self.basedir, coll_name)
        if not os.path.isdir(coll_path):
            raise RuntimeError(f"Collection directory `{coll_path}` is missing")

    def _validate_resource_id(self, coll_name, resource_id):
        """
        Make sure the collection and resource exists
        """
        self._validate_coll_name(coll_name)
        res_path = os.path.join(self.basedir, coll_name, resource_id)
        if not os.path.isdir(res_path):
            raise RuntimeError(f"Resource '{resource_id}' located at `{res_path}` does not exist.")

    def fetch_error(self, coll_name, resource_id):
        """
        Fetch the Python stack trace for a resource, if present
        """
        resource_id = str(resource_id)
        self._validate_resource_id(coll_name, resource_id)
        err_path = os.path.join(self.basedir, coll_name, resource_id, _ERR_FILENAME)
        if not os.path.isfile(err_path):
            return ''
        with open(err_path) as fd:
            return fd.read()

    def fetch_log(self, coll_name, resource_id):
        """
        Fetch the run log for a resource, if present
        """
        resource_id = str(resource_id)
        self._validate_resource_id(coll_name, resource_id)
        log_path = os.path.join(self.basedir, coll_name, resource_id, _LOG_FILENAME)
        if not os.path.isfile(log_path):
            return ''
        with open(log_path) as fd:
            return fd.read()

    def _resource_status(self, coll_name, resource_id):
        """
        Fetch stats for a single resource
        """
        resource_id = str(resource_id)
        self._validate_resource_id(coll_name, resource_id)
        res_path = os.path.join(self.basedir, coll_name, resource_id)
        status_path = os.path.join(res_path, _STATUS_FILENAME)
        with open(status_path) as fd:
            status = fd.read()
        return status

    def _coll_status(self, coll_name):
        """
        Fetch stats for a whole resource
        """
        self._validate_coll_name(coll_name)
        coll_path = os.path.join(self.basedir, coll_name)
        subdirs = os.listdir(coll_path)
        total = len(subdirs)
        pending = 0
        completed = 0
        error = 0
        unknown = 0
        for subdir in subdirs:
            stat_path = os.path.join(coll_path, subdir, _STATUS_FILENAME)
            if not os.path.isfile(stat_path):
                unknown += 1
                continue
            with open(stat_path) as fd:
                status = fd.read()
            if status == 'completed':
                completed += 1
            elif status == 'pending':
                pending += 1
            elif status == 'error':
                pending += 1
            else:
                unknown += 1
        return {
            'counts': {
                'total': total,
                'pending': pending,
                'completed': completed,
                'error': error,
                'unknown': unknown
            }
        }

    def find_by_status(self, coll_name, status='completed'):
        """
        Return a list of resource ids for a collection based on their current status
        """
        self._validate_coll_name(coll_name)
        coll_dir = os.path.join(self.basedir, coll_name)
        ids = []
        for resource_id in os.listdir(coll_dir):
            status_path = os.path.join(coll_dir, resource_id, _STATUS_FILENAME)
            with open(status_path) as fd:
                status = fd.read()
            if status == status:
                ids.append(resource_id)
        return ids

    def fetch(self, coll_name, ident, args=None, recompute=False):
        """
        Compute a new entry for a resource, or fetch the precomputed entry.
        """
        if coll_name not in self.collections:
            raise RuntimeError(f"No such collection: {coll_name}")
        start_time = int(time.time() * 1000)
        # Return value
        ret: dict = {'start_time': start_time, 'end_time': None, 'result': None, 'status': 'pending'}
        ident = str(ident)
        res = self.collections[coll_name]
        func = res['func']
        dirpath = res['dir']
        entry_path = os.path.join(dirpath, ident)
        ret['paths'] = {
            'base': entry_path,
            'error': os.path.join(entry_path, _ERR_FILENAME),
            'log': os.path.join(entry_path, _LOG_FILENAME),
            'status': os.path.join(entry_path, _STATUS_FILENAME),
            'start_time': os.path.join(entry_path, _START_FILENAME),
            'end_time': os.path.join(entry_path, _END_FILENAME),
            'result': os.path.join(entry_path, _RESULT_FILENAME),
            'storage': os.path.join(entry_path, _STORAGE_DIRNAME),
        }
        os.makedirs(entry_path, exist_ok=True)
        os.makedirs(ret['paths']['storage'], exist_ok=True)
        # Check the current status of the resource
        if os.path.exists(ret['paths']['status']):
            with open(ret['paths']['status']) as fd:
                ret['status'] = fd.read()
        # Check if it's already computed
        result_path = os.path.join(entry_path, _RESULT_FILENAME)
        if not recompute and ret['status'] == 'completed':
            with open(result_path) as fd:
                print(f'Resource "{ident}" in "{coll_name}" is already computed')
                ret['result'] = json.load(fd)
            with open(ret['paths']['start_time']) as fd:
                ret['start_time'] = int(fd.read())
            with open(ret['paths']['end_time']) as fd:
                ret['end_time'] = int(fd.read())
            return ret

        # Compute the resource
        print(f'Computing resource "{ident}" in "{coll_name}"')
        # Write placeholder files
        to_overwrite = [_RESULT_FILENAME, _ERR_FILENAME, _LOG_FILENAME, _END_FILENAME]
        for fn in to_overwrite:
            _touch(os.path.join(ret['paths']['base'], fn), overwrite=True)
        # Write out status and start time
        with open(ret['paths']['status'], 'w') as fd:
            fd.write('pending')
        print(f"Wrote to {ret['paths']['status']}")
        _write_time(ret['paths']['start_time'], ts=start_time)
        # Clear the error file
        _touch(ret['paths']['error'])
        if args is None:
            args = {}
        ctx = Context(coll_name, entry_path)
        try:
            ret['result'] = func(ident, args, ctx)
        except Exception:
            # There was an error running the resource's function
            format_exc = traceback.format_exc()
            with open(os.path.join(entry_path, _ERR_FILENAME), 'a') as fd:
                fd.write(format_exc)
            with open(ret['paths']['status'], 'w') as fd:
                fd.write('error')
            ret['end_time'] = _write_time(ret['paths']['end_time'])
            ret['status'] = 'error'
            return ret
        ret['status'] = 'completed'
        with open(result_path, 'w') as fd:
            json.dump(ret['result'], fd)
        # Write to status file
        with open(ret['paths']['status'], 'w') as fd:
            fd.write('completed')
        ret['end_time'] = _write_time(ret['paths']['end_time'])
        return ret


class Context:
    """
    This is an object that is passed as the last argument to every resource function.
    Supplies extra contextual data, if needed, for computing the resource.
    """

    def __init__(self, coll_name, base_path):
        self.subdir = os.path.join(base_path, _STORAGE_DIRNAME)
        # Initialize the logger
        self.logger = logging.getLogger(coll_name)
        fmt = "%(asctime)s %(levelname)-8s %(message)s (%(filename)s:%(lineno)s)"
        time_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, time_fmt)
        log_path = os.path.join(base_path, _LOG_FILENAME)
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)
        print(f'Logging to {log_path} -- {self.logger}')


def _write_time(path, ts=None):
    """
    Write the current time in ms to the file at path.
    Returns the generated timestamp.
    """
    if not ts:
        ts = int(time.time() * 1000)
    with open(path, 'w') as fd:
        fd.write(str(ts))
    return ts


def _touch(path, overwrite=False):
    """Write a blank file to path. Overwrites."""
    if overwrite or not os.path.exists(path):
        with open(path, 'w') as fd:
            fd.write('')
