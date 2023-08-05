Star Wars API ETL
=================

Using the Star Wars API:

1. Find the ten characters who appear in the most Star Wars films
2. Sort those ten characters by height in descending order (i.e., tallest first)
3. Produce a CSV with the following columns: name, species, height, appearances
4. Send the CSV to httpbin.org
5. Create automated tests that validate your code


Execute the exercise
--------------------
After installing the app (instructions bellow), you can execute the full code and see the result with:
"`swapietl execute_exercise`" command.

If you want to see
the full logs, execute it with `-v` : "`swapietl execute_exercise -v`"

To execute the tests (unit tests) you will need:

- python 3.x
- pip: `pip3` if your machine has `pip` for Python2.7 already installed.
- tox: Can be installed through pip3

Tox has the next jobs defined:

- `flake8`: Execute a flake8 code-check
- `py{version}`: Where `version` is the python version, for example `py37`.

*NOTE*: This solution does not provide integration tests for now.


How to install the app
======================
The application is packaged using python setuptools. All the requirements are directly
defined inside the `setup.py` file except those needed for executing the tests (note
that the test files are not packaged within the application, so it doesn't make sense
having the `test_require` definition on the setup file).

Install the application following one of these methods:

Non development mode
--------------------
- Using pip without cloning the repository:
   `pip install ./`

- Using oficial remote pip server:
   `pip install swapietl`

- With python setuptools from source files:
   `python setup.py install`

Development mode
----------------
- With pip using editable mode:
   `pip install ./ -e`

- With python setuptools using development mode:
   `python setup.py develop`


How to run the app
==================
Once you've installed the application, you can start executing commands from bash.
The application has one *console_script* created: `swapietl` if you want to enable debug logs execute it with `-v` flag (`swapietl -v`)

The application can be executed in two different modes explained bellow.

Run the application in command line mode
----------------------------------------
Using the "`swapietl $command $arg1 $arg2`" where `$command` is the function you want to execute and `$arg1` and `$arg2` the arguments.

So, for example, if you want to get the top ten characters that appeared in films, you can execute:
`swapietl get_top_characters top=10`

And, if you want to get them sorted and export the results to a csv you can:
`swapietl get_top_characters top=10 and sort_by height and export_to_csv`

NOTE: You can execute multiple commands by using the "*and*" special word.

Run the application in REPL mode
--------------------------------
The `swapietl` with no commands will bring you a REPL mode (interactive) where you can execute one by one
the possible commands with different parameters. It also brings you extra functionality as for example: autocomplete,
suggestions (in case of misspelled command).

List of available commands
==========================
Here's the list of possible commands you can execute with `swapietl` (also listed with `swapietl help`):

- `get_top_characters`: Retrieve the results from the exercise and save them into the app context.
- `sort_by attribute='height' reverse=True`: Sort previous results by a given attribute.
- `export_to_csv filename="~/results.csv"`: Export the results from the app context into a file.
  By default the filename is "~/results.csv".
- `upload_file_to filename="~/results.csv" url="http://httpbin.org/post"`: Upload the file using requests library
- `execute_exercise`: Execute the full exercise.
