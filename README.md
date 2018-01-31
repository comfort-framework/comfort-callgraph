# COMFORT CallGraph
### Description
COMFORT CallGraph tracks the execution of the tests and generates a call graph based on it. It
provides one plug-in for [nose](https://github.com/nose-devs/nose) and a second plugin 
for [py.test](https://github.com/pytest-dev/pytest). After you have called any of these test programs with your tests, 
a .callgraph file is generated, which can then be used as input for the CallGraphLoader of the 
[COMFORT framework](https://github.com/comfort-framework/comfort). 
This file includes coverage information based on each test method that is executed.

### Build
From within the directory call
```bash
python setup.py install
```

### Test
From within the directory call
```bash
make test
```

### Use
You can just call your tests like always, but just including one/two more command line loaderOptions.
- For nose call: 
```bash
nosetests --with-callgraph --callgraph-package=<root_of_project_to_track> <path_to_tests>
```

- For pytest call: 
```bash
py.test --callgraph=<root_of_project_to_track> <path_to_tests>
```