# Tutorial for writing modules

In this tutorial, we will demonstrate how to write the modules for
IOCBIO Kinetics.

Let us assume, that we have experimental data recorded on sarcomere
shortening of a cardiomyocyte and our recording equipment produced a
file with the following structure

```
# Header info
# Date: 2020-01-27
# Time: 15:46
# Experiment name: some trace 1
0.0  2.0
0.01 2.0 start of experiment
0.02 1.99
0.03 1.98
...
1.0 2.0 second beat
1.01 2.0
...
```

In the example file format, data is preceded with the header
information. After the header, we get sarcomere shortening data
through list of points, one per line. Each point contains `time` and
`sarcomere_length` (the both as floats) and, sometimes, the name of an
event as a string.

The example dataset is available [here](tutorial/demodataset.txt) and
in the main repository under
[docs/tutorial](https://gitlab.com/iocbio/kinetics/tree/master/docs/tutorial)
together with the example code. In the end of the tutorial, we will be able
to analyze the data as shown below.

![tutorial screenshot](img/tutorial-screenshot.png)


## Preparing for writing modules

Let us prepare a folder where we will put all our modules. For now,
let us find where IOCBIO Kinetics is installed and make a folder under
modules: `modules/tutorial`. All the modules which we put into that
folder will be loaded automatically and called as required by the main
program.


## Reader

As a first module, we will write a reader plugin. Let us call it
`reader.py` and put into `modules/tutorial` folder.

As it is a reader plugin, let us state that we want to use that
API. For that, in the top of `reader.py` file, let's add designation
of the plugin (`IocbioKineticsModule` variable) and corresponding
reader function declaration:

```python
IocbioKineticsModule = ["reader"]

def create_data(database, experiment_id=None, args=None):
    print("Hello from my new reader")
    return None
```

As it is, if we run `iocbio-kinetics` now, the plugin will be loaded
by the program. On our data import, we will a message "Hello from my
new reader" in the terminal output, but no data would be shown.

To import the data, let us write a reader function first. This
function will take the input string as an input (later we will explain
why) containing full file.

At the beginning, we will check, if the data is of our type:

```python
def reader(txt):
    lines = txt.splitlines()
    if not lines[0].startswith("# Header info"):
       return None, None, None
    ...
```

Thus, we will proceed with the import only for our expected dataset
and will not try to import data not covered by that reader.

Let us now load the metadata describing the experiment as a continuation of `reader` function:
```python
    data = {}
    li = 1
    while lines[li].startswith("# "):
        # split into maximally 2 elements, key and value
        # the first 2 chars are '# ' and we skip them
        processed = lines[li][2:].split(":", 1)
        if len(processed) != 2:
            break
        # store key,value pair after removing whitespaces
        data[ processed[0].strip() ] = processed[1].strip()
        # move to the next line
        li += 1
```

and proceed with loading of the data into the intermediate
variables. Note that we are going to store events together with the
time moment they occur:
```python
    events = {}
    x = []
    y = []
    while li < len(lines):
        # split into maximally 3 elements, key, value, and event
        processed = lines[li].split("\t", 2)
        if len(processed) < 2:
            # maybe a trailing line in the end of experiment
            break
        time = float(processed[0])
        sl = float(processed[1])
        x.append(time)
        y.append(sl)
        if len(processed)==3:
	   e = processed[2].strip()
           if len(e) >= 1:
               # storing event as a dictionary
               events[time] = processed[2]
        # move to the next line
        li += 1
    data['events'] = events
    return data, numpy.array(x), numpy.array(y)
```

Thus, as a result, we can get data text parsed and returned in form
of: dictionary that contains metadata and events; x and y data vectors
for time and sarcomere length, respectively.

Now we can start formulating `create_data` as requested by modules
API.

In the beginning of `create_data` we have to make sure we load it from
the correct source. Namely, this function can be called in the case we
import the data for the first time - in this case file path is given
as one of the arguments - or while user is browsing experiments. In
the latter case, `experiment_id` argument will be specified.

So, the first step is to get the data loaded into the text:

```python
def create_data(database, experiment_id=None, args=None):
    filename=getattr(args, "file_name", None)
    fulltxt=None
    if experiment_id is not None:
        fulltxt = ExperimentTutorial.get_fulltxt(database, experiment_id)

    if filename is not None:
        fulltxt = open(filename, 'r').read()

    # check if we can load anything
    if fulltxt is None: return None
```

Here, we called a static member of a class that we will have to write
later and which can load data from the database if needed. So, if the
data cannot be loaded, we return `None` to indicate that this is not
experiment that can be analyzed with this reader. However, if the data
is loaded, we proceed to reading it with our `reader` function:
```python
    d, x, y = reader(fulltxt)
    # check if data was imported
    if d is None: return None
```

Again, in the case if it was a wrong data format, the reader is
returning `None, None, None` and we return `None` as a result of
`create_data`.

After loading the data, we have to generate `experiment_id`, in case
if we loaded data from file. This has to be unique and possible to
calculate again from the data text. Hence we use a hash with a prefix:
```python
    # calculate experiment id if needed
    if experiment_id is None:
        expid = "tutorial sarcomere length - " + hashlib.sha256(fulltxt.encode('utf-8')).hexdigest()
    else:
        expid = experiment_id
```

For reference, we will add file name to our configuration description
```python
    # add filename to the data object
    d["this_file"] = filename
```

Finally, before creating `Data` object, we need to put our dataset in
the expected form:
```python
    # store data in expected format
    dd = { 'sarcomere_length': { 'x': x,
                                 'y': Carrier('Sarcomere length', 'um', y) } }
```

In this dictionary, we have experiment type (`sarcomere_length`) as a
key to the dataset consisting of `x` and `y` coordinates. Out of
those, `y` has to be stored with the `Carrier` object to link its
numerical values with the name of the measured function, its unit, and
value.

Next, we construct `Data` object that will be carried around in the
program to process the data:
```python
    data = Data( expid,
                 # any type of configuration used in the analysis further
                 config=d,
                 # specific type of experiment, may mention hardware
                 type="Tutorial experiment Sarcomere Shortening",
                 # more generic type of experiment
                 type_generic = "Sarcomere shortening",
                 # datetime string
                 time = d["Date"] + " " + d["Time"],
                 # name of experiment
                 name = d["Experiment name"],
                 # x-axis data
                 xname = "Time", xunit = "seconds",
                 xlim = (x[0], x[-1]),
                 # measured data
                 data = dd )
```

After the data is imported, we need to ensure that we can load it
again if the user is browsing the datasets in the program. For that,
we check if the record has been stored in the database first and, if
it is not, we will store all required information to the database:
```python
    # check if we have data in the database. If not, store it
    if not ExperimentGeneric.has_record(database, data.experiment_id):
        # set database into read/write mode as we import the data
        database.set_read_only(False)
        # store the data
        ExperimentTutorial.store(database, data, fulltxt)
```

As our dataset is small, we will store it in full text format. This
will be done in the class `ExperimentTutorial` that we will have to
write next.

However, our `create_dataset` is ready and it can return its result
`data` in the end:
```python
    return data
```


# Helper class: ExperimentTutorial

As we have seen while writing a reader plugin, we need the means to
find out whether our dataset is already available and store
information regarding it if its new import. Let us write a class
`ExperimentTutorial` and store it in `experiment.py` in
`modules/tutorial` folder.

For storing data, we have to prepare database table first. Together
with loading and storing, all these operations don't require any
objects to be stored, as such. Thus, we will be using static methods
grouped in a class for our convenience.

Let us start with the definition of the table used for storage:

```python
class ExperimentTutorial(ExperimentGeneric):

    database_table = "tutorial_data"

    @staticmethod
    def database_schema(db):
        db.query("CREATE TABLE IF NOT EXISTS " + db.table(ExperimentTutorial.database_table) +
                 "(experiment_id text PRIMARY KEY, rawdata text, filename text, title text, " +
                 "FOREIGN KEY (experiment_id) REFERENCES " + db.table(database_table_experiment) + "(experiment_id) ON DELETE CASCADE" +
                 ")")

    ...
```

In this definition, we first declare variable `database_table` that we
will use throughout the class to be sure that we define the table name
only once. That way it will be easy to change it in future and, if
needed, to get that name in the implementation of functionality in
other files.

The table name given by us in `database_table` could be processed by
the database engine interface
(`iocbio.kinetics.io.db.DatabaseInterface`). For example, for
compatibility with other tables in the lab database, it maybe prefixed
with some string. We use `kinetics_` as a prefix to all tables
generated by IOCBIO Kinetics resulting in the table name
`kinetics_tutorial_data` for the table generated in this class.

Next, we create the table only if it does not exists. The
`database_schema` method will be called on every application startup
and we have to ensure it works every time.

Creation of a table is given through SQL query. API to write queries
is provided by Python package
[Records](https://pypi.org/project/records/). In short, you just call
`query` method on the database object and state the query as a
text. It is possible to provide arguments to specify conditions, as we
will show below. Here, no arguments are needed, so query is rather
simple.

When adding records to this table, we refer to another table
(`database_table_experiment`) where global experiment Id is
defined. Notice that on deletion of the record in the main table
(`database_table_experiment`), we will delete the record in the
`tutorial_data` table as well. This is recommended for data
consistency and ensuring that you can remove data entered by mistake
easily.

All other variables saved in the table are for keeping full file
content (`rawdata`), name of the file and the title of experiment
assigned by researcher.

To call the `database_schema` method on start of the program, we just
have to state that this file is a module of `database_schema` type and
define the function which is required by its API:

```python
IocbioKineticsModule = ["database_schema"]

# class definition
...

# definition of database_schema function
def database_schema(db):
    # just in case if our experiment is the first one, make general if needed
    ExperimentGeneric.database_schema(db)
    # create table for our experiment
    ExperimentTutorial.database_schema(db)
```
With the table declared and ready, let's write functions that are
responsible for loading and storing the data. In these functions, we
will use a unique hardware flag that will help us easily to identify
whether the experiment is of a type which is covered by the
`ExperimentTutorial` class. In this case, we will use
`tutorial_hardware` as a flag:

```python
class ExperimentTutorial(ExperimentGeneric):
    ...

    @staticmethod
    def get_fulltxt(database, experiment_id):
        # check if the record with the experiment_id exists and reflects our hardware
        if ExperimentGeneric.hardware(database, experiment_id) != 'tutorial_hardware':
            return None
        print('Loading raw data for experiment:', experiment_id)
        # read in the raw text
        for q in database.query("SELECT rawdata FROM " + database.table(ExperimentTutorial.database_table) +
                                " WHERE experiment_id=:experiment_id",
                                experiment_id=experiment_id):
            return q.rawdata
        return None
```

Data reading starts with a check whether the hardware is indeed
covered by our reader. For that we use a simple wrapper provided by
`ExperimentGeneric` to request the hardware description. If it is not
defined (hardware will be `None`) or different, we will just return
`None` as a result of the function.

If the hardware is defined, we expect to get a single record from the
database with it. However, to keep simple access to the Records API,
we will request that record as a result of a query, which will return
all results matching it. As shown above, we request `rawdata` from the
table `ExperimentTutorial.database_table` that would match given
experiment ID. To introduce conditions, we use facilities provided by
Records through use of `:experiment_id` tag and specification of its
value as a keyword argument to `query`
(`experiment_id=experiment_id`). Result is available in row-by-row
basis and accessible as an attribute, as shown above.

As we expect only one result, we return it as soon as we get it. In
case if there is no record regarding the experiment, `None` is
returned in the end.

To store the data, we will use the following:

```python
class ExperimentTutorial(ExperimentGeneric):
    ...

    @staticmethod
    def store(database, data, fulltxt):
        experiment_id = data.experiment_id

        # store reference to the experiment in generic table
        ExperimentGeneric.store(database, experiment_id, time=data.time,
                                type_generic=data.type_generic,
                                type_specific=data.type, hardware="tutorial_hardware")

        c = database

        if not database.has_record(ExperimentTutorial.database_table,
                                   experiment_id = experiment_id):
           c.query("INSERT INTO " + database.table(ExperimentTutorial.database_table) +
                   "(experiment_id, rawdata, filename, title) " +
                   "VALUES(:experiment_id,:ftxt,:fname,:exptitle)",
                   experiment_id=experiment_id,
                   ftxt=fulltxt,
                   fname=data.config["this_file"],
                   exptitle=data.config["Experiment name"])
```

As shown above, we will store first in the general table describing
all experiments in the database. For that, we use
`ExperimentGeneric.store` with the arguments required by that
method. It is here we define that our hardware is called
`tutorial_hardware`.

As for raw data, we store it using `INSERT` SQL statement. However,
before that, we check whether the record is there already. For that,
there is a simple wrapper to an SQL statement that checks existence of
a record and requires database table name together with the keyword
argument consisting of column in the table (key) and the value of that
column (value). In our case, column name (`experiment_id`) is the same
as the name of the variable containing the value we are interested in.

As soon as we confirmed that there is no record in the table, we
insert the raw data. Notice that the `INSERT` statement is again using
tags in it and has the corresponding tag values defined through
keyword arguments. This is a syntax that is recommended for many
reasons, including simplicity and security (prevention of SQL
injection) to name the few.


# Analyzer for primary data

Our experiment has sarcomere length shortening recorded during a
single beat. Let us find the time constants associated with each
contraction and the amplitude. For that, we will use an analyzer which
was specifically written for such type of oscillations -
`AnalyzerBump`. Our analyzer will be derived from
`AnalyzerBumpDatabase` that has already interface with the database
and all we will have to do is to make some specific adjustments for
our case.

For the analyzer, we will need new file (`primary.py`) and store it in
`modules/tutorial` folder.

As we use `iocbio.kinetics.calc.bump.AnalyzerBumpDatabase` as a base
class, writing the analyzer is rather simple and we just have to
initialize the base class properly by pointing it to the relevant
data.

Object of the primary analyzer class are created for each region of
interest selected by the user. Thus, this object has to take care of
fitting the data and storing the analysis results. In addition,
primary analyzers are used to slice the data when requested by user
into the region through dedicated static methods.

Let us start with the data fitting aspect of the function.

```python
class AnalyzerTutorialPrimary(AnalyzerBumpDatabase):

    database_table = "tutorial_primary"

    @staticmethod
    def database_schema(db):
        AnalyzerBumpDatabase.database_schema(db, AnalyzerTutorialPrimary.database_table, peak=False)

    def __init__(self, database, data):
        # initialization of base class
        AnalyzerBumpDatabase.__init__(self, database,
                                      # name of the database table used to store data
                                      AnalyzerTutorialPrimary.database_table,
                                      # data and corresponding x- and y- arguments
                                      data, data.x('sarcomere_length'), data.y('sarcomere_length').data,
                                      # we look at shortening, not increase. For bump, it means that peak is False
                                      peak=False,
                                      # units of the value
                                      valunit=data.y('sarcomere_length').unit)
        self.axisnames = XYData(data.xname, data.y('sarcomere_length').name)
        self.axisunits = XYData(data.xunit, data.y('sarcomere_length').unit)
        # when searching for time to peak, we need reference value for it
        self.update_reference_time(data)
        # fit data
        self.fit()
```

As with the `ExperimentTutorial` above, we define the table name as a
part of the class attribute. This allows later to refer to the table
simply, as we will see below.

In initialization, we have to define few variables for the base
class. For start, we have forward name of the table, give full dataset
and x- and y- values of the points fitted. In our case, the reader
defined the dataset as

```python
    dd = { 'sarcomere_length': { 'x': x,
                                 'y': Carrier('Sarcomere length', 'um', y) } }
```

So, we get access to the numpy vectors via
`data.x('sarcomere_length')` and, in case of the carriers as used to
transfer measured values, via `data.y('sarcomere_length').data`. As
the bump function can be either used to fit temporary increase in a
value (bump in its classical sense) or decrease, the parameter `peak`
specifies whether an increase is expected. As we fit sarcomere
shortening, aka reduction in length, we set `peak=False`.

Next, we have to define axis names and units. In addition, before data
fitting, we have to define reference time point. This point is used to
find relative position of a peak in the bump. In our case, we will use
the event time, if available inside region of interest, as a reference
point. As we will use the reference point calculations in several
locations, let's define it as a method:

```python
class AnalyzerTutorialPrimary(AnalyzerBumpDatabase):
    ...

    def update_reference_time(self, data):
        x0, x1 = data.xlim()
        events = data.config['events']
        # default reference
        self.t_reference = 0
        for et, ev in events.items():
            if et > x0 and et < x1:
                # the first reference within the region of interest
                self.t_reference = et
                break
```

As it is shown above, we get the events from the configuration defined
by our reader. In the reader, we made a list of events consisting of
tuples in form of `(time,event)`. Due to our file format, events are
already sorted according to time. The events list is used now to find
the first event within the region of interest (`x0` and `x1` define
range) and set the reference time accordingly. The attribute
`t_reference` is defined and used later in the base class.

As a last part of the initialization, we call `fit` method:
```python
class AnalyzerTutorialPrimary(AnalyzerBumpDatabase):
    ...

    def fit(self):
        AnalyzerBumpDatabase.fit(self, n=3, points_per_node=4, max_nodes=25)
```

In our case, it is rather trivial forwarding to the base class method
with few specified parameters. The base class will then fit the data,
write the results into the database table, and, to inform the other
modules and the main program, fire a Qt signal calling others to
update. These steps would have to be performed in our analysis class
if the base class would not have provided it.

Next, we have to define behavior in the case when users will move or
change the region of interest or rename the event.

Change in the region of interest will result in the call of
`update_data`. In response to the change, we have to find new
reference time, refresh data vectors in the base class, and fit the
new data:

```python
class AnalyzerTutorialPrimary(AnalyzerBumpDatabase):
   ...

   def update_data(self, data):
        # called when user is moving regions of interest
        self.update_reference_time(data)
        # update data in base class
        AnalyzerBumpDatabase.update_data(self, data.x('sarcomere_length'), data.y('sarcomere_length').data)
        # fit the data
        self.fit()
```

As a response to the change in event string, `update_event` is
called. In our case, we have events as "Beat beatnumber" and we will
process them by separating event into words and using the second one
as a value. As we will need such conversion in several locations,
let's define corresponding helper method as well:

```python
class AnalyzerTutorialPrimary(AnalyzerBumpDatabase):
    ...

    def update_event(self, event_name):
        self.data.event_name = event_name
        self.data.event_value = AnalyzerTutorialPrimary.eventvalue(event_name)

    @staticmethod
    def eventvalue(event_name):
        try:
            # events are in form "beat Number"
            evalue = float(event_name.split()[1])
        except:
            evalue = None
        return evalue
```

With this, we have covered all analyzer functionality required to
analyze a single region of interest. To assist with the creation of
the regions of interest, we need to define how data is sliced into the
regions.

First, a static method `slice` has to be defined which takes full
dataset and x-axis limits as an argument. The method is expected to
return the sliced data. In practice, we offload slicing to the data
object itself and have only to implement our experiment-specific
events handling. So, in our case `slice` is very simple:

```python
class AnalyzerTutorialPrimary(AnalyzerBumpDatabase):
    ...

    @staticmethod
    def slice(data, x0, x1):
        # create a slice of data
        sdata = data.slice(x0, x1)
        # determine event corresponding to the data if any
        events = data.config['events']
        # default, if we don't find any
        sdata.event_name = ""
        sdata.event_value = None
        for et, ev in events.items():
            if et > x0 and et < x1:
                # the first reference within the region of interest
                sdata.event_name = ev
                sdata.event_value = AnalyzerTutorialPrimary.eventvalue(ev)
                break
        return sdata
```

Such proportion -- one-line statement for data slicing and longer
handling of events to fill attributes `event_name` and `event_value`
-- is typical. These attributes are recorded by the main program in a
specific table that defines all regions of interest. Later we will see
how they can be used.

Second, as a last method of the analyzer class, we have to define
`auto_slicer`. This is a method that takes full dataset and splits it
into the regions of interest. It is used when you import the data
first time and is expected to assist users by pre-defining the
regions. Strictly, it can just return empty list, if not
desired. However, routine analysis will be simplified if it is done in
accordance with the experiment. In our case, we will split the data
according to the events. We assume that one beat is once per second,
according to our pacing. As a default regions of interest, we will
take 0.9 seconds and will start it 0.05 seconds before the event in the
dataset:

```python
class AnalyzerTutorialPrimary(AnalyzerBumpDatabase):
    ...

    @staticmethod
    def auto_slicer(data):
        events = data.config['events']
        # no events in data, nothing to make slices with
        ekeys = list(events.keys())
        ekeys.sort()
        if len(ekeys) == 0: return []

        sliced_data = []
        width = 0.9
        offset = 0.05
        for et in ekeys:
            sdata = AnalyzerTutorialPrimary.slice(data, et-offset, et-offset+width)
            sliced_data.append(sdata)
        return sliced_data
```

Notice that we slice the data by calling our `slice` method defined
earlier. As for rest, it is based on the formulation of events that we
used in our reader.

With the class `AnalyzerTutorialPrimary` defined, we have to declare
that it is a module and define it accordingly:

```python
### Module flag
IocbioKineticsModule = ['analyzer']

... class definition ...

# Module API
def analyzer(database, data):
    Analyzer = {}
    if data.type_generic == "Sarcomere shortening":
        # as a key, we define type of ROI used later in secondary analyzers as well
        Analyzer['default'] = AnalyzerTutorialPrimary
    # only primary analyzer is returned this time
    return Analyzer, None, None
```

Few notes regarding `analyzer` function. This function returns three
values as a tuple: the primary analyzer, the secondary analyzer
showing results on plots, the secondary analyzer showing results in
statistics tables. If some of the analyzers are missing, they can be
returned as `None` or empty carriers (dictionary or list, as expected
by API). Here, we return only the primary analyzer. Hence, the second
and the third return values are `None`.

The primary analyzer has to be returned as a name of the class in the
dictionary. The key of the dictionary defines _roi type_. There can be
multiple regions of interest types with each having separate x-axis
interval. In our case, we use only one type and call it
`default`. Notice that the same type, when wishing to show data on the
secondary analysis plot has to be used for the corresponding secondary
analyzer. But more about it later.

In the beginning of `analyzer` function, we check that the experiment
type is the one that we want to analyze. Here we used `type_generic`
attribute with the comparison to the value as we specified in the
reader. The rest is filling the dictionary accordingly and returning
it.

As the analyzer requires table in the database, let us define it also
as database_schema module and change the code by adding this type to
`IocbioKineticsModule` and defining corresponding function:

```python
IocbioKineticsModule = ['analyzer', 'database_schema']

...
# definition of database_schema function
def database_schema(db):
    AnalyzerTutorialPrimary.database_schema(db)
```

And with that, we finished our first analyzer.




# Secondary analyzer

The secondary analyzers are used to analyze results of the primary
one. For that, the secondary analyzer will use only the data provided
through the database by the primary analyzer(s).

In our case, let us try to fit with a linear function the change in
beat duration as a function of the beat number. For that, we will use
the parameters calculated by `AnalyzerBump`: time between the peak and
the time-moments when the sarcomere length was at 50% of its bump
amplitude (before and after).

The results of the primary analyzer are stored in a table with
`data_id`, `type`, `value` where `data_id` is a unique ID for region
of interest, `type` corresponds to the statistic calculated by the
analyzer, and `value` to the value of the statistic. In our case, the
types we are interested in are `before 50` and `after 50`.

For the analyzer, we will need new file (`secondary.py`) and store it in
`modules/tutorial` folder.

In this case, while we will fit the data using `AnalyzerLinRegress`,
we will deal with the database and signaling inside our class. For
signaling, used to inform the main program the data has changed, we
have to define helper class

```python
from PyQt5.QtCore import pyqtSignal, QObject

# General signaling class
class AnalyzerTutorialSignals(QObject):
    sigUpdate = pyqtSignal()
```

With that defined, we can proceed to definition of our secondary
analyzer:
```python
class AnalyzerTutorialSecondary(AnalyzerLinRegress):

    database_table = 'tutorial_duration_linregress'

    @staticmethod
    def database_schema(db):
        db.query("CREATE TABLE IF NOT EXISTS " + db.table(AnalyzerTutorialSecondary.database_table) +
                 "(experiment_id text not null PRIMARY KEY, " +
                 "slope double precision not null, intercept double precision, " +
                 "FOREIGN KEY (experiment_id) REFERENCES " + db.table(database_table_experiment) + "(experiment_id) ON DELETE CASCADE)")

    def __init__(self, database, data):
        AnalyzerTutorialSecondary.database_schema(database)
        # initialization of base class: start with empty data
        AnalyzerLinRegress.__init__(self, [], [])
        # create signals attribute
        self.signals = AnalyzerTutorialSignals()
        # store connection to the database
        self.database = database
        # store experiment_id
        self.experiment_id = data.experiment_id
        # define axes
        self.axisnames = XYData("Beat No", "Duration")
        self.axisunits = XYData("#", "s")
        # fetch data from the database
        self.get_data()
        # fit data
        self.fit()
```

As before, we define database table name and create it if its not
available already. Note that this time we refer not to the table
defining regions of interests (`database_table_roi`), as in the
primary analyzer done internally by `AnalyzerBumpDatabase`, but to the
table defining experiment ID. As with the raw data storage, we will
remove our record if the experiment is deleted from the main table.

In the `__init__`, we start with creating the table, initializing the
base class without any data to fit at the beginning, creating `signal`
attribute as expected by API, store required data, and proceed to the
analysis. Analysis consists of two parts: fetching the data via
`get_data` and fitting it.

When getting the data, the main complexity is formulation of SELECT
statement. In this case, we have to join the primary analysis table
with itself to get `before 50` and `after 50` available at the same
time. The data we are interested in is of the analyzed experiment
only, so that we use for filtering using a table `database_table_roi`
which has `experiment_id`, `data_id`, `x0`, `x1`, `event_name`,
`event_value` on each record. When fetching the data from the
database, we check that the beat has a number and, if it does, use it
for fitting:

```python
class AnalyzerTutorialSecondary(AnalyzerLinRegress):
    ...

    def get_data(self):
        c = self.database
        beat = []
        duration = []
        for row in c.query(
"""select b.data_id, b.value + a.value as duration, r.event_name, r.event_value AS beat_nr
from %s b
join %s a on b.data_id=a.data_id
join %s r on b.data_id=r.data_id
where a.type='after 50' and b.type='before 50' and r.experiment_id=:experiment_id""" % (c.table(AnalyzerTutorialPrimary.database_table),
                                                                                       c.table(AnalyzerTutorialPrimary.database_table),
                                                                                       c.table(database_table_roi)),
                experiment_id = self.experiment_id):
            n = row.beat_nr
            d = row.duration
            if n is not None:
                beat.append(n)
                duration.append(d)
        self.experiment = XYData(np.array(beat), np.array(duration))
```

Within this function, we end up storing the points used in the fit as
`self.experiment` using `XYData`. `XYData` takes two arguments which
are each numpy arrays (can be of string as well when defining axis
names and units).

With `self.experiment` filled, we can proceed to fitting the data and
filling statistical information we want to show as a table:

```python
class AnalyzerTutorialSecondary(AnalyzerLinRegress):
    ...

    def fit(self):
        AnalyzerLinRegress.fit(self)
	if self.intercept is None or self.slope is None:
	    return # data are not ready
        c = self.database
        # do we need to update or insert?
        if self.database.has_record(AnalyzerTutorialSecondary.database_table, experiment_id=self.experiment_id):
            c.query("UPDATE " + c.table(AnalyzerTutorialSecondary.database_table) +
                    " SET slope=:slope, intercept=:intercept WHERE experiment_id=:experiment_id",
                    slope=self.slope, intercept=self.intercept, experiment_id=self.experiment_id)
        else:
            c.query("INSERT INTO " + c.table(AnalyzerTutorialSecondary.database_table) +
                    "(experiment_id, slope, intercept) VALUES(:experiment_id,:slope,:intercept)",
                    experiment_id=self.experiment_id, slope=self.slope, intercept=self.intercept)
        self.stats['linreg slope'] = Stats("Slope", "seconds/beat", self.slope)
        self.stats['linreg intercept'] = Stats("Intercept", "seconds", self.intercept)
        self.signals.sigUpdate.emit()
```

In the fit, we first perform the fitting using the base class and then
store the results in the database. Notice that we check whether record
exists and then either update or insert it.

With the data stored, we show the results to the user by updating
`stats` attribute. Behind the scenes, in `AnalyzerLinRegress`,
`self.calc` has been updated as well to be able to show it next to the
experimental data on plots. That base class also filled some
information regarding the fit as a part of `self.stat`.

As it is shown in the example, `self.stat` is a dictionary with the
values describing statistics using a label, units, and the value. The
key in the dictionary is used to sort the data shown in the table and
can be adjusted accordingly. Here we prefixed the key strings to
ensure that the slope and intercept are shown next to each other to
the user.

Method `fit` is also called during data updates. When compared to the
primary analyzer, the data update is done using the database queries
only:
```python
class AnalyzerTutorialSecondary(AnalyzerLinRegress):
    ...

    def update(self):
        self.get_data()
        self.fit()

```

As before, we have to define access function for the module API and
its type:

```python
IocbioKineticsModule = ['analyzer']
...
def analyzer(database, data):
    if data.type_generic == "Sarcomere shortening":
        p = AnalyzerTutorialSecondary(database, data)
        # as a key, we define type of ROI used later in secondary analyzers as well
        return None, { 'default': p }, [p]
    return None, None, None
```

Compared to the primary analyzer, there are few differences. First, we
do not declare database schema module, but create the table only when
the corresponding object is initialized. This is possible as the
analyzer results are not used by others. In the opposite case, we have
to define tables using database_schema module type.

Second, instead of giving the class name, we create an object and pass
it as a secondary analyzer. This is due to the difference between the
primary and secondary analyzers. The primary analyzers have an object
per region of interest while the secondary only one object per
experiment. So, it can be immediately created.

As shown in `analyzer` above, we returned the analyzer as a part of a
dictionary (key is the type of region of interest as defined in the
primary analyzer module) and a list. Here, the dictionary is used to
show the analyzer fit results on the secondary analyzer plot (requires
`self.experiment` and `self.calc`) while the list to show data in the
statistics table (`self.stats` is required). It is common that the
analyzers showing some data on the plots are also showing something in
the tables. However, some analyzers (like min/max determination) show
data in the table only.

This concludes the tutorial. See [Modules API](modules.api.md)
description for a formal way of presenting the API as well as for
details not covered over here.
