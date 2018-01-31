import logging
import os

from nose.plugins import Plugin
from nose.util import tolist

from callgraph.control import SeppelCallGraphController, _settrace

log = logging.getLogger('nose.plugins.callgraph')


class CallGraphPlugin(Plugin):
    name = 'callgraph'

    def options(self, parser, env=os.environ):
        super(CallGraphPlugin, self).options(parser, env=env)
        parser.add_option("--callgraph-paths", action="append",
                           default=env.get('NOSE_TRACE_PATH'),
                           metavar="TRACEPATHS",
                           dest="trace_paths",
                           help="Restrict traced calls to selected paths "
                                "[NOSE_TRACE_PATH]")
        parser.add_option("--callgraph-output", action="store",
                           default=env.get('NOSE_CALLGRAPH_OUTPUT', '.callgraph'),
                           dest="callgraph_output",
                           help="Location of output file")

    def configure(self, options, conf):
        super(CallGraphPlugin, self).configure(options, conf)

        self.conf = conf
        self.tracePaths = []
        if options.trace_paths:
            if isinstance(options.trace_paths, (list, tuple)):
                trace_paths = options.trace_paths
            else:
                trace_paths = [options.trace_paths]

            for pkgs in [tolist(os.path.expanduser(x)) for x in trace_paths]:
                self.tracePaths.extend(pkgs)

        if self.tracePaths:
            log.info("Tracing will only be done for paths: %s", self.tracePaths)

        if self.enabled:
            self.output = options.callgraph_output

            self.seppel_callgraph = SeppelCallGraphController(log, self.tracePaths)
            _settrace(self.seppel_callgraph.trace_calls)

    def report(self, stream):
        self.seppel_callgraph.write(self.output)