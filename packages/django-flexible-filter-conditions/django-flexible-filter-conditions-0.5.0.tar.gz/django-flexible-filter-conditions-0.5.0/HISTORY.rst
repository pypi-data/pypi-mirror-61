.. :changelog:

History
-------

0.5.0 (2020-02-19)
++++++++++++++++++

* refactor: remove filter_by_condition(), make it NamedCondition class method filter_by_query()
* fix contains operator
* add more testing

0.4.0 (2020-02-18)
++++++++++++++++++

* added support for new operators: in, list, date
* mutlipe conditions in one named comdition can be added to support
  subsequent filters
* add xor operator
* add negate to condtition (and remove nor)


0.3.0 (2020-01-23)
++++++++++++++++++

* fixes and improvements for better user orientation


0.2.0 (2020-01-21)
++++++++++++++++++

* Added blank paremeter value
* Added isnull filter

0.1.0 (2020-01-14)
++++++++++++++++++

* First release on PyPI.
