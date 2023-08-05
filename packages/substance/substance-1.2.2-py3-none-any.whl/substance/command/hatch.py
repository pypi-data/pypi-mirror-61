import subprocess
import os
import random
import string
import urllib.request, urllib.parse, urllib.error
try:
    import readline  # Make raw_input nicer to use, but don't make it required
    readline
except ImportError:
    pass  # Optional dependency
from substance import (Command)
from substance.logs import (logging)
from substance.config import (Config)

logger = logging.getLogger(__name__)


class Hatch(Command):

    def getUsage(self):
        return "substance hatch [options] TEMPLATE [REVISION]"

    def getHelpTitle(self):
        return "Create a new project based on a git or tarball template."

    def getHelpDetails(self):
        return "\n".join([
            "Arguments:",
            "  TEMPLATE     Git repository, or short name. Examples of valid TEMPLATEs:",
            "               php-project        (resolves to https://github.com/turbulent/template-php-project)",
            "               bob/my-template    (resolves to https://github.com/bob/my-template)",
            "               ssh://git@gitlab.turbulent.ca:6666/templates/heap-project.git",
            "               https://www.example.com/path/to/tarball.tar.gz",
            "               file:///home/bob/my-git-template-directory",
            "",
            "  REVISION     Refers to the git ref of the template repository. Defaults to 'master'."
        ])

    def getShellOptions(self, optparser):
        optparser.add_option("-s", "--strip", dest="strip", default="1",
                             help="Strip X number of leading components from tarball paths", action="store_true")
        return optparser

    def main(self):
        tpl = self.getArg(0)
        if not tpl:
            return self.exitError("You MUST provide a template name or git repository URL!")
        ref = self.getArg(1) or "master"

        target_dir = "".join(tpl.split('/')[-1:]).split('.')[0]

        if not tpl.startswith('ssh://') and not tpl.startswith('https://') and not tpl.startswith('file://'):
            splt = tpl.split("/", 2)
            if len(splt) == 2:
                tpl = 'https://github.com/%s/%s/archive/%s.tar.gz' % (
                    splt[0], splt[1], ref)
                target_dir = splt[1]
            else:
                target_dir = tpl
                tpl = 'https://github.com/turbulent/template-%s/archive/%s.tar.gz' % (
                    tpl, ref)
        install_dir = os.getcwd() + ("/%s" % target_dir)
        if os.path.exists(install_dir):
            print("\n!!! Install directory exists! Make sure it's empty or Some files may be overwritten !!!\n")

        print("You are about to hatch a new project.")
        print("  Template used: %s" % tpl)
        print("  Ref (version): %s" % ref)
        if not tpl.endswith('.tar.gz'):
            print("  Ref (version): %s" % ref)
        print("  Path         : %s" % install_dir)
        print("")

        if not self.confirm("Are you SURE you wish to proceed?"):
            return self.exitOK("Come back when you've made up your mind!")

        if not os.path.exists(install_dir):
            os.mkdir(target_dir, 0o755)
        os.chdir(target_dir)
        print("Switching to directory: %s" % install_dir)
        print("Downloading template archive...")
        if tpl.endswith('.tar.gz'):
            # With tar archives, everything is usually packaged in a single directory at root of archive
            strip = int(self.getOption('strip'))
            urllib.request.urlretrieve(tpl, 'tpl.tar.gz')
        else:
            strip = 0  # git archive never packages in a single root directory
            if self.proc(['git', 'archive', '--verbose', '-o', 'tpl.tar.gz', '--remote=' + tpl, ref]):
                return self.exitError('Could not download template %s@%s!' % (tpl, ref))

        print("Extracting template archive...")
        if self.proc(['tar', '--strip', str(strip), '-xf', 'tpl.tar.gz']):
            return self.exitError('Could not extract template archive!')

        # Acquire list of files
        print("Getting list of files in template...")
        out = subprocess.check_output(['tar', '-tf', 'tpl.tar.gz'], universal_newlines=True)
        tplFiles = ['/'.join(l.split('/')[strip:]) for l in out.split('\n') if l]
        tplFiles = [l for l in tplFiles if os.path.isfile(l)]

        print("Cleaning up template archive...")
        if self.proc(['rm', 'tpl.tar.gz']):
            return self.exitError('Could not unlink temporary template archive!')

        # At this point, we have all the files we need
        hatchfile = os.path.join('.substance', 'hatch.yml')
        if os.path.isfile(hatchfile):
            config = Config(hatchfile)
            res = config.loadConfigFile()
            if res.isFail():
                return self.exitError("Could not open %s for reading: %s" % (hatchfile, res.getError()))

            # Execute pre-script if any
            for cmd in config.get('pre-script', []):
                print(cmd)
                subprocess.call(cmd, shell=True)

            vardefs = config.get('vars', {})
            # Autogenerate a secret
            chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
            variables = {
                '%hatch_secret%': ''.join(random.SystemRandom().choice(chars) for _ in range(32))
            }
            if vardefs:
                print("This project has variables. You will now be prompted to enter values for each variable.")
                for varname in vardefs:
                    val = ''
                    required = vardefs[varname].get('required', False)
                    default = vardefs[varname].get('default', '')
                    description = vardefs[varname].get('description', '')
                    while not val:
                        val = input("%s (%s) [%s]: " % (
                            varname, description, default))
                        if default and not val:
                            val = default
                        if not required:
                            break
                    variables[varname] = val

            summary = "\n".join(["  %s: %s" % (k, variables[k])
                                 for k in list(variables.keys())])
            print("Summary: ")
            print(summary)
            if not self.confirm("OK to replace tokens?"):
                return self.exitOK("Operation aborted.")

            print("Replacing tokens in files...")
            sed = "; ".join(["s/%s/%s/g" % (k, variables[k].replace('/', '\\/'))
                             for k in list(variables.keys())])
            for tplFile in tplFiles:
                if self.proc(['sed', '-i.orig', sed, tplFile]):
                    return self.exitError("Could not replace variables in files!")
                bakFile = tplFile + ".orig"
                if os.path.isfile(bakFile):
                    if self.proc(['rm', bakFile]):
                        logger.warn(
                            "Could not unlink backup file %s; you may have to remove it manually.", bakFile)

            # Execute post-script if any
            for cmd in config.get('post-script', []):
                print(cmd)
                subprocess.call(cmd, shell=True)

            # Remove hatchfile
            if self.proc(['rm', hatchfile]):
                return self.exitError('Could not unlink %s!' % hatchfile)

        print("Project hatched!")
        return self.exitOK()

    def proc(self, cmd, variables=None):
        logger.debug(subprocess.list2cmdline(cmd))
        return subprocess.call(cmd)

    def confirm(self, prompt):
        confirm = ''
        while confirm not in ('Y', 'y'):
            confirm = input("%s (Y/n) " % prompt) or 'Y'
            if confirm in ('N', 'n'):
                return False
        return True
