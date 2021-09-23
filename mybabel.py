#! /usr/bin/python3
#
# This code is in the public domain.
#
# This is a wrapper around 'pybabel' that sets our include path
# to find the 'i18nfix' module.  It takes the name of the
# pybabel program as the first argument (must be a Python script!)
# and passes the other arguments to pybabel after setting our
# sys.path.
#
import shutil
import sys

# First, extend the search path as needed (without setting PYTHONPATH!)
sys.path.insert(0, ".")

# Now, find the actual pybabel program in the $PATH
pb=shutil.which(sys.argv[1])

# Remove 'pybabel' from argv[] so that pybabel doesn't confuse
# itself for the first command-line argument ;-)
sys.argv.remove(sys.argv[1])

# Now we can run pybabel. Yeah!
exec(compile(source=open(pb).read(), filename=pb, mode='exec'))
