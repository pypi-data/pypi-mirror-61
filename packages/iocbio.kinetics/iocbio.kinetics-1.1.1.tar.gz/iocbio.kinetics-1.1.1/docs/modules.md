# Modules 

Data analysis and reading from different formats is supported via
modules. This allows to extend the functionality of the program via
defined APIs to cover specific experimental protocols. Here, we cover
all the types of the modules and show, using an artificial example,
how to write new ones.

Before proceeding with the tutorial and description of module details,
few general notes that have to be taken into account. Modules are
written in Python and are loaded recursively from
`iocbio.kinetics.modules` and any other folder specified in program
settings. This allows you to structure modules according to your
experiments and put all modules dealing with the same type of
experiment together in the same folder.

When modules are loaded, all `iocbio.kinetics` objects have to be
imported using absolute path. For example,
```python
from iocbio.kinetics.handler.experiment_generic import ExperimentGeneric
```
All module Python files, have to be loaded using relative path, as in
```python
from .experiment_spectro import ABC
```
By following this simple rule, you will ensure that the correct code
gets loaded and your modules will not depend on internal
implementation used to load them.


## Module types

Modules can be of several types to cover different type of processing
done by them. In practice, module types define how the application
accesses them and at which part of the analysis. Each Python file
can contain multiple APIs and cover several types as well. Its also
possible to have Python files that are just dependency of some module
file and, in that case, the type of that dependency file should be left
unspecified.

Module type is defined using global variable in that module -
`IocbioKineticsModule` as

```python
IocbioKineticsModule = ["args", "database_schema"]
```

where `IocbioKineticsModule` is a list with elements describing a
type. For each module type declared in Python file, we have to define
specific function with the given API that will be called by the
application. Below, is the table summarizing available modules and the
functions called by application.

| Type                 | API Function         | Comment                                                   |
|----------------------|----------------------|-----------------------------------------------------------|
| `analyzer`           | `analyzer`           | Analysis of experimental data                             |
| `args`               | `args`               | Parameters for protocols given in addition to raw data    |
| `database_info`      | `database_info`      | Info field in the data overview                           |
| `database_schema`    | `database_schema`    | Definition of database tables                             |
| `database_processor` | `database_processor` | Additional database processing after import of experiment |
| `reader`             | `create_data`        | Import of experimental data                               |


Modules API is described in a [formal way](modules.api.md) and via
[tutorial](modules.tutorial.md). The tutorial describes in details how
to write new modules using an artificial dataset as an example.
