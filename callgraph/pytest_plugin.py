import logging
import os

from nose.util import tolist

from callgraph.control import SeppelCallGraphController, _settrace

log = logging.getLogger('pytest.plugins.callgraph')


def pytest_addoption(parser):
    """Add options to control coverage."""

    group = parser.getgroup(
        'callgraph', 'callgraph reporting')
    group.addoption('--callgraph-paths', action='append', default=[], metavar='path',
                    nargs='?', const=True, dest='trace_paths',
                    help='get traces for filesystem path '
                         '(multi-allowed)')
    group.addoption('--callgraph-output', dest='callgraph_output', action='store', default='.callgraph',
                    help='output file for callgraph data. '
                         'default: .callgraph')


def pytest_configure(config):
    """Activate plugin if appropriate."""
    if config.getvalue('trace_paths'):
        if not config.pluginmanager.hasplugin('_callgraph'):
            plugin = Plugin(config.option)
            config.pluginmanager.register(plugin, '_callgraph')


class Plugin(object):

    def __init__(self, options):
        self.trace_paths = []
        if isinstance(options.trace_paths, (list, tuple)):
            trace_paths = options.trace_paths
        else:
            trace_paths = [options.trace_paths]

        for pkgs in [tolist(os.path.expanduser(x)) for x in trace_paths]:
            self.trace_paths.extend(pkgs)

        if self.trace_paths:
            log.info("Tracing will only be done for paths: %s", self.trace_paths)

        self.output = options.callgraph_output
        self.seppel_callgraph = SeppelCallGraphController(log, self.trace_paths)
        _settrace(self.seppel_callgraph.trace_calls)

    def pytest_terminal_summary(self):
        self.seppel_callgraph.write(self.output)
