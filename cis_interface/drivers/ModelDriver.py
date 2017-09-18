#
# This should not be used directly by modelers
#
import os
import subprocess
import sys
from pprint import pformat
from cis_interface.drivers.Driver import Driver
from cis_interface import backwards


def preexec():  # pragma: no cover
    # Don't forward signals - used to ignore signals
    os.setpgrp()


class ModelDriver(Driver):
    r"""Base class form Model drivers.

    Args:
        name (str): Driver name.
        args (str or list): Argument(s) for running the model on the command
            line.
        is_server (bool, optional): If True, the model is assumed to be a server
            and an instance of :class:`cis_interface.drivers.RMQServerDriver`
            is started. Defaults to False.
        client_of (str, list, optional): THe names of ne or more servers that
            this model is a client of. Defaults to empty list.
        \*\*kwargs: Additional keyword arguments are passed to parent class's
            __init__ method.

    Attributes (in additon to parent class's):
        args (list): Argument(s) for running the model on the command line.
        process (:class:`subprocess.Popen`): Process used to run the model.
        is_server (bool): If True, the model is assumed to be a server and an
            instance of :class:`cis_interface.drivers.RMQServerDriver` is
            started.
        client_of (list): The names of server models that this model is a
            client of.

    """

    def __init__(self, name, args, is_server=False, client_of=[],
                 **kwargs):
        super(ModelDriver, self).__init__(name, **kwargs)
        self.debug(str(args))
        if isinstance(args, str):
            self.args = [args]
        else:
            self.args = args
        self.process = None
        self.is_server = is_server
        if isinstance(client_of, str):
            client_of = [client_of]
        self.client_of = client_of
        self.env.update(os.environ)

    def run(self):
        r"""Run the model on a new process, receiving output from."""
        self.debug(':run %s from %s with cwd %s and env %s',
                   self.args, os.getcwd(), self.workingDir, pformat(self.env))
        with self.lock:
            try:
                self.process = subprocess.Popen(
                    ['stdbuf', '-o0'] + self.args, bufsize=0,
                    stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE,
                    env=self.env, cwd=self.workingDir, preexec_fn=preexec)
            except:  # pragma: debug
                self.exception('(%s): Exception starting in %s with wd %s',
                               self.args, os.getcwd, self.workingDir)
                return
        
        # Re-direct output
        while True:
            with self.lock:
                if self.process:
                    line = self.process.stdout.readline()
                else:
                    return
            if not line:
                break
            sys.stdout.write(backwards.bytes2unicode(line))
            sys.stdout.flush()
            
        self.debug(':run: done')

    def terminate(self):
        r"""Terminate the process running the model."""
        self.debug(':terminate()')
        with self.lock:
            if self.process:
                self.debug(':terminate(): terminate process')
                self.process.terminate()
                self.process = None
        super(ModelDriver, self).terminate()
