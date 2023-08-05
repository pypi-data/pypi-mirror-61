=========
Changelog
=========

Version 0.2.8
=============

- add dependencies in the setup. When a user pip install this package, the dependencies will be installed too automatically.


Version 0.2.7
=============

- introduced ``ValueFromExternalDfFeature`` that allows to merge a column coming from an external dataframe.


Version 0.2.6
=============

- introduced ``MultiComponentFeature`` that allows to map n features into one single column through a lambda function


Version 0.2.5
=============

- introduced the one component feature ``WeekdayFromDateFeature``


Version 0.2.4
=============

- ``DependenciesError.to_string()`` method does not report anymore as victims the columns which have an empty list of missing dependencies


Version 0.2.3
=============

- ``InputDataError`` now returns example of wrong format values when the to_string() method is used


Version 0.2.2
=============

- ``MonthFromDateFeature`` now accepts both ``DateTimeInputFeature`` and ``DateInputFeature`` as input



Version 0.2.1
=============

- Fixed an unexpected behaviour for which the input features with allow_nan received a wrong format if nan values
  were passed into the verify_input method


Version 0.2.0
=============

- Introduced the class ``StackFactory`` with the method ``clones`` that can be used to
  generate a stack of identical features with different arguments. This can be very useful
  when we are handling a multitude of features and we want to apply similar operations
  to them. E.g.

  .. code:: python

    import pandas as pd

    from features_factory.input_features import IntInputFeature, FloatInputFeature
    from features_factory.one_component_features import OneComponentFeature
    from features_factory.stack_factory import StackFactory

    int1 = IntInputFeature('int1')
    int2 = IntInputFeature('int2')
    float1 = FloatInputFeature('float1')

    names = ['2 x int1', '2 x int2', '2 x float1']
    dependencies = [int1, int2, float1]
    args = [{'name': name, 'dependency': feat, 'map_function': lambda x: 2*x}
            for name, feat in zip(names, dependencies)]
    stack = StackFactory.clones(OneComponentFeature, args)

    df = pd.DataFrame({int1.name(): [3, 5, 7], int2.name(): [15, 20, 50], float1.name(): [2.2, 0.1, 5.5]})
    df = stack.with_depende    ncies().insert_into(df)
    print(df)
    #    int1  int2  float1  2 x float1  2 x int1  2 x int2
    # 0     3    15     2.2         4.4         6        30
    # 1     5    20     0.1         0.2        10        40
    # 2     7    50     5.5        11.0        14       100



Version 0.1.0
=============

- Introduced ``StringTimestampInputFeature``, an input feature representing a string encoding a timestamp. To verify that the string actually encode a timestamp the class use the following procedure:

  - if no format has been specified then use ``pd.to_datetime`` to interpret the strings. If no error is raised, then it assumes that all the values can be encoded into a datetime object.

  - if a format has been specified then use ``datetime.datetime.strptime()``, and if no error are raised, then it assumes that all the values can be encoded into a datetime object.

- Introduced ``DateFromStringFeature``, which is almost the same as ``DateTimeFromStringFeature`` but converts the string int  o a date instead of a datetime object

- All the input features which are subclass of ``ProvidedInputFeatureWithControlOnNaN`` can now be specified with the ``allow_nan=True`` optional parameter (default is ``False``). In this case, NaN are not considered for the sake of error. E.g.:

  .. code:: python

      import pandas as pd
      from features_factory.input_features import IntInputFeature

      feat = IntInputFeature('feat', allow_nan=True)
      df = pd.DataFrame({'feat': [1, None, 3]})
      input_error = feat.verify_input(df)
      print(input_error.is_empty())
      # True

- Introduced ``RenamedFeature``. It simply add a column to the DataFrame which is identical
  to the original one, but with a new name. E.g.:

  .. code:: python

    import pandas as pd
    from features_factory.input_features import IntInputFeature
    from features_factory.one_component_features import RenamedFeature

    feat = IntInputFeature('int')
    renamed_feat = RenamedFeature('renamed', feat)

    df = pd.DataFrame({'int': [1, 2, 3]})
    df = renamed_feat.insert_into(df)
    print(df)
    #    int  renamed
    # 0    1        1
    # 1    2        2
    # 2    3        3



Version 0.0.0
=============

- Very first release
