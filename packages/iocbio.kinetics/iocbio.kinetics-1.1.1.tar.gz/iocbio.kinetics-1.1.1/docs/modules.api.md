# Modules API

Modules, as used by the application, have to be given of one of the
expected types. Below, is the description of each of the types with
the expected arguments and the return values.

## Module type: analyzer

This module is used to provide analyzers for given data. For this
module, in the corresponding Python file, specify

```
IocbioKineticsModule = ["analyzer"]
```

and function

```python
def analyzer(database, data):
    ...
    return Analyzer, overall_plot, overall_stats
```

The function arguments are
* `database` of type `iocbio.kinetics.io.db.DatabaseInterface`
* `data` of type `iocbio.kinetics.io.data.Data`

These argument variables would allow analyzers to decide whether they
are interested in that particular dataset by quering `data` type,
database with the `data.experiment_id` and/or other means.

The returned values of all analyzer modules will be combined together
to form the sets used to analyze the data. Any of the returned tuple
can be `None`. It is expected that if the data is not analyzed by this
module, return value will be `None, None, None`.

Out of returned values, `Analyzer` and `overall_plot` are
dictionaries, `overall_stats` is a list. Each of the return values is
described below.

### `analyzer` return value: `Analyzer`

`Analyzer` is a dictionary with the key designating ROI type and the
value corresponding to the primary analyzer class. There could be only
one primary analyzer class for a given type of ROI. If there are
multiple defined, only the last one used in the scan of all modules
will be used.

While there is only one analyzer class expected per ROI type, one can
combine analyzers by deriving the analyzer from `AnalyzerCompose`
class.

The object of the class pointed by the dictionary, will be constructed
as needed and should provide the following interface (replace
`AnalyzerPrimary` as appropriate):

```python
class AnalyzerPrimary(AnalyzerGeneric):
      
      def __init__(self, database, roi_data):
          ...
          self.database = database
          self.data = roi_data
          self.experiment = XYData(x, y)
          self.axisnames = XYData("x axis", "y axis")
          self.axisunits = XYData("x units", "y units")
          self.signals.sigUpdate = pyqtSignal()
          ...
          # fit the data
          self.calc = XYData(..., ...)
          self.stats = { key: value, ... }
          self.signals.sigUpdate.emit()
          
      def remove(self):

      def update_data(self, data):
      
      def update_event(self, event_name):
      
      @staticmethod
      def slice(data, x0, x1):

      @staticmethod
      def auto_slicer(data):

```

When instantiated via `__init__`, the analyzer object corresponds to
one of the regions of interest selected by the user. So, it gets the
Data object pointing to that region only with the ROI ID specified in
`data.data_id`. During initialization, analyzer is expected to perform
all calculations, fill the attributes accordingly and emit the update
signal. All the results should be written into the database using
`database`. As it is expected that the database records need updates
in response to the update events, `database` connection should be
stored as an attribute `self.database`.

The attributes `axisnames` and `axisunits` define the name and units
of x- and y-axes. For that, they are expected to use
`iocbio.kinetics.calc.generic.XYData` type.

Same `XYData` type is used for attributes `experiment` and `calc` for
transferring numerical values for experimental and fitted data as
`numpy.array`. The values are shown on primary analysis graph for
visual inspection of the fit by user. Note that this requires that the
lengths of the vectors should comply with
`experiment.x.length==experiment.y.length` and
`calc.x.length==calc.y.length`. Experiment and calc vectors don't have
to be of the same size.

The attribute `stats` should be of dictionary with the keys used only
to sort the shown data. Values of the dictionary should be of type
`iocbio.kinetics.calc.generic.Stats`.

Signal `self.signals.sigUpdate` should be emitted every time the fit
or data has been changed. This is used to update graphs and statistics
tables accordingly.

Method `remove` should delete all the records in the database
corresponding to the ROI which is analyzed by the object. This
corresponds to the database table(s) used by this analyzer only. It is
called in response to the user's request to remove ROI.

Method `update_data` should use given `data` to update its
`experiment`'s `x` and `y` values, fit them and update statistics
together with `calc` attributes. Updated results should also written
to the database.

Method `update_event` is used to update event string associated with
ROI. It is called in response to the user's changes in event string
and are expected to be processed by the analyzer. Results should be
written by updating `self.data.event_name` and
`self.data.event_value`. Analyzer is not expected to write events into
the database, this is done in the main program by checking the set
attributes.

There are two static methods which are required to slice the data into
ROIs.

Static method `slice` is called when new ROI is requested. It is
expected that the method will call `data.slice(x0, x1)` and use the
returned sliced data. The main task of the analyzer is to fill slice
data `event_name` and `event_value` attributes according to the
experiment and return sliced data as a return value.

Static method `auto_slicer` is called when the new experiment is
imported and is expected to return a list of sliced datasets as a
return value. Example cases include splitting the data according to
the events in `data.config["events"]` or, if the experimental protocol
has known sequence, splitting by pre-defined sequence. It is expected
that `auto_slicer` will determine intervals `(x0,x1)` and call static
method `slice` with those intervals to populate the list. If there is
no apparent way of splitting data automatically or, as a use for the
first implementation, `auto_slicer` can also return an empty list. It
would still allow user's to make new ROIs from GUI.


### `analyzer` return value: `overall_plot`

`overall_plot` is a dictionary with the key designating currently
active ROI type and the value corresponding to the secondary analyzer
object (note that it is not a class as for `Analyzer`, but
object). There could be only one secondary analyzer object for a
specified type. 

The analyzers specified in `overall_plot` are the ones that analyze
the primary analysis results and show the data in the plot on the
right bottom of GUI. It is frequently that the same object is also
included into `overall_stats`, as described in a separate sub-section
below.

Each object of `overall_plot` analyzer should be of the class with the
API mostly covering a subset of the classes used for `Analyzer`:

```python
class AnalyzerOverallPlot(AnalyzerGeneric):
      
      def __init__(self, database, roi_data):
          ...
          self.database = database
          self.data = roi_data
          self.experiment = XYData(x, y)
          self.axisnames = XYData("x axis", "y axis")
          self.axisunits = XYData("x units", "y units")
          self.signals.sigUpdate = pyqtSignal()
          ...
          # fit the data
          self.calc = XYData(..., ...)
          self.signals.sigUpdate.emit()
          
      def update(self):
```

While most of the methods are the same as in `Analyzer`, notice the
absence of `remove` and absence of any data passed to `update`. This
reflects the secondary analysis nature of the analyzer - it is
expected to get the data from the database with the primary analysis
results.

The method `update` is called if any of the ROIs or the results of the
current primary analyzer has been updated.

It is expected that the analysis results are calculated on
initialization and on updates. The results are expected to be stored
in the database tables.

For the meaning of attributes, see description of `Analyzer` above.


### `analyzer` return value: `overall_stats`

`overall_stats` is a list of the secondary analyzer objects (note that
it is not a class as for `Analyzer`, but object). There could be as
many secondary analyzer objects as needed.

The analyzers specified in `overall_stats` are the ones that analyze
the primary analysis results and show the data in the plot on the
right bottom of GUI. 

Each object of `overall_stats` analyzer should be of the class with the
API mostly covering a subset of the classes used for `Analyzer`:

```python
class AnalyzerOverallStats(AnalyzerGeneric):
      
      def __init__(self, database, roi_data):
          ...
          self.database = database
          self.data = roi_data
          self.signals.sigUpdate = pyqtSignal()
          ...
          # fit the data
          self.stats = { key: value, ... }
          self.signals.sigUpdate.emit()
          
      def update(self):
```

As for `overall_plot`, notice the absence of `remove` and absence of
any data passed to `update`. This reflects the secondary analysis
nature of the analyzer - it is expected to get the data from the
database with the primary analysis results.

The method `update` is called if any of the ROIs or the results of the
current primary analyzer has been updated.

For the meaning of attributes, see description of `Analyzer` above.



## Module type: args

This module is used to compose command line arguments of kinetics
program as well as its help text covering used protocols. For this
module, specify

```
IocbioKineticsModule = ["args"]
```

and function `args` with an argument that is of
`iocbio.io.arguments.Parser` type to add new arguments (if
needed):
```python
def args(parser)
```

Command line arguments for the main program and for data import dialog
can be added using `parser.add_argument` method. All arguments are
expected to be of type `str` with the type conversion done later by
the reader if needed.

Return value should be either `None` or short description of
supported protocol types. Description should end with newline.

Example implementation is shown below:

```python
def args(parser):
    parser.add_argument(name='electro_condition', help='Electrophysiology experiment condition. For example: ttx, iso')
    return '''Electrophysiology:
------------------
ltcc - Voltage step prodocol to estimate LTCC current
kill - Fluorescence maximum from killing cardiomyocyte
srcontent_by_ncx - Caffeine induced calcium relase
srrecovery_by_ltcc - SR recovery after caffeine experiment
'''

```


## Module type: database_info

This module is used to display some additional information in the list of all experiments shown by GUI on the left side
of the main window. For this module, specify

```
IocbioKineticsModule = ["database_info"]
```

and function `database_info(database)`. The function is expected to
return a string with SQL SELECT statement. The statement should return
one text value and use `e.experiment_id` to look up information in the
relevant tables, as demonstrated below in the example. `database` is
given as an argument to for access to `database.table` method. Example
implementation:

```python
def database_info(database):
    return "SELECT title from %s s where s.experiment_id=e.experiment_id" % database.table("electrophysiology")
```



## Module type: database_schema

This module is used to initialize database schema. For this module, specify

```
IocbioKineticsModule = ["database_schema"]
```

and function `database_schema(database)`. The function is expected to
initialize database tables, if needed. Here, `database` is of type
`iocbio.kinetics.io.db.DatabaseInterface`.

There return value, if any, is not used.


## Module type: database_processor

This module is used to apply some operations to the database after
loading datasets during the initial import from files, as given in
command line arguments. For example, this allows to link new imported
dataset with some lab-specific preparation ID.

For this module, specify

```
IocbioKineticsModule = ["database_processor"]
```

and function `database_process(database, data, args)`. It is possible
that data argument is `None` during a call with the processor function
expected to check for it if needed. Function is called after the data
was created on the basis of the command line arguments.

While `database` and `data` are of the same type as in the analyzer
functions above, `args` is given as `AttrDict`. It allows to access
options via attributes or through `[key]` as for dictionaries.


## Module type: reader

This module is used to read data from file or database and create data
object. For this module, specify

```
IocbioKineticsModule = ["reader"]
```

and function `create_data`:

```python
create_data(database, experiment_id=None, args=None)
```

The function should return `None` if the dataset is not of the type
covered by this reader. Otherwise, `data` is expected as a return
value of type `iocbio.kinetics.io.data.Data`.

The function can be called either with command line arguments `args`
or with `experiment_id` specified, but never both different from
`None`. With `experiment_id` specified, data should be loaded from
database according to that `experiment_id`.

For `args`, if specified, the function can assume that all global
options, such as `file_name` and `protocol` are available. `args` is
AttrDict with the access available through keys (as in
`attr['file_name']) and attributes (as in `args.file_name`). Before
accessing, it is recommended to test whether the key/attribute exists
(use `args.get` and `args.getattr` methods).

When loading the data, the first module that will return non-None
value and load the data will be considered as responsible for that
data type. In this case, none of the subsequent reader modules will be
called and the returned data will be used for analysis.
