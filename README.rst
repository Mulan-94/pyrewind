PyRewind

This package arose as a consequence of a circumstance rather. It was 
occasioned by a situation I had a few days ago, whereby I needed to rerun 
tests I had done some time at the end of last year, on a python package that 
I am developing . Re-running the tests required me to rollback on some of the 
software's dependencies. While I had the python dependencies installed in 
some virtual environment somewhere, It very quickly dawned on me that I may 
have upgraded some of the packages in that environment recently, and thus 
rolling back would mean downgrading all the versions of the packages 
available in the environment to the versions they were at, at the time of 
running those tests.

As at the writing of this description, pip install did not provide a way to 
install a versions of a package before a certain date. This package is an 
attempt to alleviate this problem. 

PyRewind is the shortened form of the name PyPI rewind. Given a requirements 
file, and a date, PyRewind will generate another requirement file containing 
versions of the packages in the input requirements' file prior to the 
provided date.

To install PyRewind, type:

.. code-block:: python
    pip install pyrewind
    pyrewind -h

You will be presented with the following help menu

.. code-block:: python

    usage: pyrewind [options] <value>

    Take your requirements' versions back in time :)

    optional arguments:
      -h, --help            show this help message and exit

    Required arguments:
      --before              Get versions of requirements in requirements file
                            before this date. Format must be 'dd-mm-yyyy'
      --debug               Enable debugging mode
      -if , --input-file    File containing the current requirements
      -of , --output-file   Name to give generated output file name 
                            containing the new (older) requirements. 
                            Including the file extension eg. retro.txt

To run pyrewind, input
.. code-block:: python

    pyrewind --input-file current_reqs.txt --output-file old_reqs.txt --before 20-01-2019

Please note that the date argument ``--before``, must have the format **dd-mm-yyyy**. 

Below is a sample output of what is to be expected. This input file was 
created on 2nd of June 2020, and the argument used for the before date was 
``--before 10-11-2019``.

+--------------+--------------+
| Input File   | Output file  |
+==============+==============+
| bokeh==2.0.2 | bokeh==1.4.0 |
+--------------+--------------+
| dask==2.15.0 | dask==2.7.0  |
+--------------+--------------+
| numba==0.49.0| numba==0.46.0|
+--------------+--------------+
