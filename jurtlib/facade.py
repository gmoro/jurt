from jurtlib import Error
from jurtlib import config, root, su, target as targetmod

class JurtFacade:

    rootmanager = None

    def __init__(self, config):
        self.config = config
        self.targets = targetmod.load_targets(config)

    def _get_target(self, name=None):
        if name is None:
            name = self.config.jurt.default_target
            if name == targetmod.UNSET_DEFAULT_TARGET:
                raise Error, "no target name provided and "\
                        "no default target set in configuration"
        try:
            target = self.targets[name]
        except KeyError:
            #FIXME use BuildError
            raise Error, "no such target: %s" % (name)
        return target

    def build(self, paths, targetname=None, id=None, stage=None):
        """Builds a set of packages"""
        target = self._get_target(targetname)
        target.build(paths, id=id, stage=stage)

    def target_names(self):
        return self.targets.keys()

    def shell(self, targetname=None, id=None):
        target = self._get_target(targetname)
        target.shell(id)

    def check_permissions(self, interactive=True):
        if not self.targets:
            raise Error, "no targets setup, you must have at least "\
                    "one setup in configuration for testing"
        try:
            for targetname in self.targets:
                if interactive:
                    yield "testing target %s.." % (targetname)
                self.targets[targetname].check_permissions(interactive)
                if interactive:
                    yield "OK"

        except su.SudoNotSetup:
            raise Error, ("the sudo helper for jurt is not setup, "
                    "please run as root: jurt-setup -u %s" %
                    (su.my_username()[0]))
