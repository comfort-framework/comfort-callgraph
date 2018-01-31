import logging
import sys

from callgraph.python import PythonFile

logging.basicConfig(filename='.callgraph_log', filemode='w', level=logging.DEBUG)


try:
    import threading
except ImportError:
    _settrace = sys.settrace

    def _unsettrace():
        sys.settrace(None)
else:
    def _settrace(func):
        threading.settrace(func)
        sys.settrace(func)

    def _unsettrace():
        sys.settrace(None)
        threading.settrace(None)


class SeppelCallGraphController(object):
    def __init__(self, log, trace_paths):
        self.output = []
        self.trace_paths = trace_paths
        self.log = log
        self.contexts = {}

    def add_to_output(self, line):
        self.output.append(line)

    def write(self, output_file):
        with open(output_file, 'w') as fh:
            fh.write("\n".join(self.output))

    def _get_context(self, file_name, line_no):
        if file_name in self.contexts:
            return self.contexts[file_name].context(line_no)
        else:
            try:
                file = PythonFile(file_name)
                context = file.context(line_no)
                self.contexts[file_name] = file
                return context
            except Exception:
                self.log.warning("Could not get context for file %s with line number %s" % (file_name, line_no))
                return None

    def trace_calls(self, frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code

        callee_line_no = frame.f_lineno
        callee_filename = co.co_filename
        caller = frame.f_back

        if caller is not None:
            caller_line_no = caller.f_lineno
            caller_filename = caller.f_code.co_filename

            if caller_filename.startswith(tuple(self.trace_paths)) and \
                    callee_filename.startswith(tuple(self.trace_paths)):

                callee_context = self._get_context(callee_filename, callee_line_no)
                caller_context = self._get_context(caller_filename, caller_line_no)

                if callee_context is not None and caller_context is not None and not caller_context.endswith("C)") and \
                        not callee_context.endswith("C)"):
                    self.add_to_output("%s,%s;%s,%s" % (caller_context, caller_filename, callee_context, callee_filename))
                else:
                    self.log.warning("Could not store result with callee %s and caller %s" % (callee_filename,
                                                                                              caller_filename))
        return self.trace_calls
