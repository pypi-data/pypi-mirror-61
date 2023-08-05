import os
import sys
import platform
import time
import logging
import shutil
import shlex
import subprocess
from subprocess import call, Popen, check_output, CalledProcessError
from substance.exceptions import (
    FileSystemError, ShellCommandError, UserInterruptError)
from substance.monads import *
from threading import Thread
from substance.platform import (isCygwin)

# pylint: disable=W0232

logger = logging.getLogger(__name__)


class Shell(object):

    @staticmethod
    def printConfirm(msg, assumeYes=False):
        if assumeYes:
            return OK(True)

        logger.info(msg)
        try:
            res = input('Proceed? [N/y] ')
            if res.lower().startswith('y'):
                logger.info('... proceeding')
                return OK(True)
            return Fail(UserInterruptError(message="User interrupted."))
        except KeyboardInterrupt as err:
            return Fail(UserInterruptError(message="User interrupted."))

    @staticmethod
    def call(cmd, cwd=None, shell=True, sudo=False):
        try:
            mustSleep = False
            if sudo and not shell:
                if isCygwin():
                    mustSleep = True
                    cmd = ["cygstart", "--action=runas"] + cmd
                else:
                    cmd = ["sudo"] + cmd
            logger.debug("COMMAND[%s]: %s", cwd, cmd)
            returncode = call(cmd, shell=shell, cwd=cwd)
            if returncode == 0:
                # Allow command to finish on Windows (cygstart exits early)
                return OK(None).then(lambda: None if not mustSleep else time.sleep(1))
            else:
                return Fail(ShellCommandError(code=returncode))
        except CalledProcessError as err:
            return Fail(ShellCommandError(code=err.returncode, message=err.output, stdout=err.output))

    @staticmethod
    def command(cmd):
        logger.debug("COMMAND: %s", cmd)
        try:
            out = check_output(cmd, shell=True)
            return OK(out.decode().strip())
        except CalledProcessError as err:
            return Fail(ShellCommandError(code=err.returncode, message=err.output, stdout=err.output))

    @staticmethod
    def procCommand(cmd, cwd=None):
        try:
            logger.debug("PROC COMMAND: %s", cmd)
            proc = Popen(shlex.split(cmd), shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
            pout, perr = proc.communicate()
            cmdOut = pout.decode()
            cmdErr = perr.decode()
            if proc.returncode == 0:
                return OK({"stdout": cmdOut, "stderr": cmdErr})
            else:
                return Fail(ShellCommandError(code=proc.returncode, message=cmdOut, stdout=cmdOut, stderr=cmdErr))
        except KeyboardInterrupt:
            logger.info("CTRL-C Received...Exiting.")
            return Fail(UserInterruptError())

    @staticmethod
    def readAppendFlush(stream, buffer=b'', amount=1):
        the_bytes = stream.read(amount)
        if the_bytes:
            the_bytes += byte
            sys.stdout.write(the_bytes.encode())
            sys.stdout.flush()
        return buffer

    @staticmethod
    def streamCommand(cmd, cwd=None, shell=False):
        try:
            logger.debug("STREAM COMMAND: %s", cmd)
            proc = Popen(shlex.split(cmd), shell=shell,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
            stdout = b''
            stderr = b''
            while True:
                stdout = readAppendFlush(sys.stdout, stdout, 1)
                stderr = readAppendFlush(sys.stderr, stderr, 1)

                if not d  and not de and proc.poll() is not None:
                    break

            stdout = stdout.encode()
            stderr = stderr.encode()

            if proc.returncode == 0:
                return OK({"stdout": stdout, "stderr": stderr})
            else:
                return Fail(ShellCommandError(code=proc.returncode, message=stdout, stdout=stdout, stderr=stderr))
        except OSError as err:
            err.strerror = "Error running '%s': %s" % (cmd, err.strerror)
            return Fail(err)
        except KeyboardInterrupt:
            logger.info("CTRL-C Received...Exiting.")
            return Fail(UserInterruptError())

    @staticmethod
    def execvp(cmdPath, cmdArgs, cmdEnv=None, sudo=False):
        logger.debug("EXECVPE: `%s` with environment %s",
                     subprocess.list2cmdline(cmdArgs), cmdEnv)
        if sudo:
            cmdPath = "sudo"
            cmdArgs = ["sudo"] + cmdArgs
        if cmdEnv:
            os.execvpe(cmdPath, cmdArgs, cmdEnv)
        else:
            os.execvp(cmdPath, cmdArgs)

    @staticmethod
    def stringify(cmd, env={}):
        envStr = ""
        if env:
            envStr = " ".join(["%s=%s" % (k, subprocess.list2cmdline([env[k]])) for k in env]) + " "
        return "%s%s" % (envStr, subprocess.list2cmdline(cmd))

    @staticmethod
    def chmod(path, mode):
        try:
            os.chmod(path, mode)
            return OK(path)
        except Exception as err:
            return Fail(ShellCommandError(code=1, message="Failed to chmod %s: %s" % (path, err)))

    @staticmethod
    def makeDirectory(path, mode=0o750):
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode)
                return OK(path)
            except Exception as err:
                return Fail(ShellCommandError(code=1, message="Failed to create %s: %s" % (path, err)))
        return OK(path)

    @staticmethod
    def copyFile(src, dst):
        return Try.attempt(lambda: shutil.copy(src, dst))

    @staticmethod
    def pathExists(path):
        return OK(path) if os.path.exists(path) else Fail(FileSystemError("Path %s does not exist." % path))

    @staticmethod
    def rmFile(path):
        if os.path.isdir(path):
            return Fail(FileSystemError("%s is a directory.") % path)
        return OK(os.remove(path))

    @staticmethod
    def nukeDirectory(path):
        try:
            if path and path is not '/' and path is not 'C:\\':
                shutil.rmtree(path)
            return OK(None)
        except Exception as err:
            return Fail(ShellCommandError(code=1, message="Failed to rmtree: %s: %s" % (path, err)))
