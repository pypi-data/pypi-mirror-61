================
features_factory
================

A small python package that helps dealing with Machine Learning features (using ``pandas``).



Installing the package
======================

Latest available code:

.. code:: bash

  pip install git+https://gitlab.com/francesco-calcavecchia/features_factory.git

Specific version:

.. code:: bash

  pip install git+https://gitlab.com/francesco-calcavecchia/features_factory.git@vX.Y.Z


Quickstart
==========

- Verify the input column ``country_code`` in a pandas DataFrame ``df``:

  .. code:: python

    feat = CountryCodeInputFeature('Country Code')
    input_error = feat.verify_input(df)
    input_error.has_missing_columns(), input_error.has_columns_with_nan(), input_error.has_columns_with_wrong_format()


- Map a column into another through a lambda function:

  .. code::

    original_feat = StringInputFeature('Full Name')  # declare a feature corresponding to the column
    feat = OneComponentFeature('First Name', original_feat, lambda x: x.split(' ')[0])
    enriched_df = feat.insert_into(df)


- Map two columns into one using a lambda function:

  .. code::

    original_feat1 = StringInputFeature('First Name')
    original_feat2 = StringInputFeature('Second Name')
    feat = TwoComponentFeature('Full Name', original_feat1, original_feat2, lambda r: r[0] + ' ' + r[1])
    new_df = feat.insert_into(df)



- Create a stack of features:

  .. code:: python

    original_feat1 = StringInputFeature('First Name')
    original_feat2 = StringInputFeature('Second Name')
    feat = TwoComponentFeature('Full Name', original_feat1, original_feat2, lambda r: r[0] + ' ' + r[1])
    stack = Stack([original_feat1, original_feat2, feat])


- Use a stack like a list:

  .. code::

    stack.add(feat)


  .. code::

    stack.remove(feat)


  .. code::

    print('Number of features in this stack = ', len(stack))


  .. code::

    for feat in stack:
        print(feat.name())


  .. code::

    feat = stack[1]


  .. code::

    stack = stack1 + stack2
    stack += stack3


- A stack automatically ignores duplicates:

  .. code:: python

    stack = Stack([feat1, feat2])
    stack.add([feat1])
    len(stack) == 2


- Handy stack functionalities:

  .. code:: python

    original_feat1 = StringInputFeature('First Name')
    original_feat2 = StringInputFeature('Second Name')
    feat = TwoComponentFeature('Full Name', original_feat1, original_feat2, lambda r: r[0] + ' ' + r[1])
    stack = Stack([feat])
    stack = stack.with_dependencies()
    stack.names() == ['Full Name', 'First Name', 'Second Name']


  .. code:: python

    original_feat1 = StringInputFeature('First Name')
    original_feat2 = StringInputFeature('Second Name')
    feat = TwoComponentFeature('Full Name', original_feat1, original_feat2, lambda r: r[0] + ' ' + r[1])
    stack = Stack([feat1, feat2, feat])
    stack = stack.only_inputs()
    stack.names() == ['First Name', 'Second Name']


- Verify multiple input columns:

  .. code:: python

    stack = Stack([feat1, feat2, feat3])
    input_error = stack.verify(df).get_input_data_error()


- Create a stack of features, verify the input data, the feature dependencies, and insert the feature in the df:

  .. code:: python

    # input features
    distance = FloatInputFeature('Distance [m]')
    duration = IntInputFeature('Duration [s]')
    runner_first_name = StringInputFeature('Runner First Name')
    runner_last_name = StringInputFeature('Runner Last Name')
    runner_age = IntInputFeature('Runner Age')
    # derived features
    speed = TwoComponentFeature('Average Speed [km/h]', distance, duration,
                         lambda r: 3.6*r[0]/r[1])
    full_name = TwoComponentFeature('Full Name', runner_first_name, runner_last_name,
                             lambda r: r[0] + ' ' + r[1])
    full_name_with_age = TwoComponentFeature('Full Name With Age', full_name, runner_age,
                                      lambda r: r[0] + ' (age {})'.format(r[1]))
    # final feature
    summary = TwoComponentFeature('Summary', full_name_with_age, speed,
                           lambda r: 'The runner {} run with and average speed of {} km/h'.format(r[0], r[1]))
    # create a stack
    stack = Stack([summary]).with_dependencies()
    # look for errors
    stack_error = stack.verify(df)
    # populate the df with all the features
    if stack_error.is_empty():
        new_df = stack.insert_into(df)


- Are you working with a moltitude of features and you need to apply the same operation
  to them? Check out the `StackFactory` class. E.g.

  .. code:: python

    int1 = IntInputFeature('int1')
    int2 = IntInputFeature('int2')
    float1 = FloatInputFeature('float1')

    names = ['2 x int1', '2 x int2', '2 x float1']
    dependencies = [int1, int2, float1]
    args = [{'name': name, 'dependency': feat, 'map_function': lambda x: 2*x}
            for name, feat in zip(names, dependencies)]
    stack = StackFactory.clones(OneComponentFeature, args)

    df = pd.DataFrame({int1.name(): [3, 5, 7], int2.name(): [15, 20, 50], float1.name(): [2.2, 0.1, 5.5]})
    df = stack.with_dependencies().insert_into(df)
    print(df)
    #    int1  int2  float1  2 x float1  2 x int1  2 x int2
    # 0     3    15     2.2         4.4         6        30
    # 1     5    20     0.1         0.2        10        40
    # 2     7    50     5.5        11.0        14       100



Pre-Built Features
==================

Input Features
  ``BoolInputFeature``: boolean

  ``IntInputFeature``: integer

  ``FloatInputFeature``: floating point

  ``DateTimeInputFeature``: datetime

  ``DateInputFeature``: date

  ``StringInputFeature``: string

  ``StringTimestampInputFeature``: string encoding a timestamp readable via pandas.to_datetime, or according a specific [format](https://docs.python.org/3.7/library/datetime.html#strftime-strptime-behavior)

  ``CountryCodeInputFeature``: two-digit country code (e.g. DE, IT, FR, ES)


One-Component Features
  ``OneComponentFeature``: define a new feature starting from another one, simply by specifying a lambda function

  ``RenamedFeature``: rename a feature column

  ``DateTimeFromStringFeature``: extract the datetime from a string which encodes a timestamp

  ``DateFromStringFeature``: extract the date from a string which encodes a timestamp

  ``MonthFromDateFeature``: extract the month from a date-like object

  ``WeekdayFromDateFeature``: extract the weekday from a date-like object (0=Monday, 6=Sunday)


Two-Component Features
  ``TwoComponentFeature``: define a new feature starting from two others, simply by specifying a lambda function

  ``DurationFeature``: given a start datetime and an end datetime, compute the duration


Multi-Component Features:
  ``MultiComponentFeature``: define a new feature starting from multiple other ones, simply by specifying a lambda function

Composed Features
  ``MeanValueForKeyFeature``: given a column with keys and one with values, aggregate the values according to the keys and compute their averages. Finally assign the averages to the new column, according to the keys.



Why You Should Use This Library
===============================

- **data verification is a rather painful and tricky task. This library can help in many ways**:

  #. make you think about it

  #. let you use some checks that others already used that can help you identify issues, like missing columns, presence of NaN, and wrong data format

  #. how many times did it happen that you check the data and they seem ok, but then you modify them somehow, don't check them again (because what should have changed?) but something goes wrong? With this library you build a stack that let you make this verification in a very simple manner, avoiding these situations.

- often **features are built one on top of another creating a rather complicated tree of dependencies** that can be annoying to manage manually. This library lets you define the features structure, and then take care of everything for you.

- think for a moment about how many times **people wrote again and again the same verification code** for a feature, or the code to generate one. And how many times stupid mistakes led to a big waste of time? The idea of this open source library is to avoid this.

- using this library will force you to a **separation of concepts**. Using it, your code will look cleaner.


Developers should know
======================

- Set up the right PYTHONPATH:

  .. code:: bash

    export PYTHONPATH=$(pwd)/src

- To setup a new virtualenv starting from the Pipfile:

  .. code:: bash

    pipenv install                    # create the virtualenv
    pipenv shell                      # activate the virtualenv


  If you want to update the environment using the Pipfile.lock run:

  .. code:: bash

    pipenv sync                       # activate the virtualenv

- If you need to install a new python package, use ``pipenv`` instead of ``pip``.

- To run the tests, execute:

  .. code:: bash

    python -m unittest discover tests
