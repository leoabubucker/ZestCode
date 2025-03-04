import subprocess, os

read_the_docs_build = os.environ.get('READTHEDOCS', None) == 'True'

if read_the_docs_build:

    # subprocess.call('cd ../doxygen; doxygen', shell=True)
    # Run Doxygen to generate XML before building Sphinx docs
    subprocess.call('doxygen', shell=True)

    # Sphinx extensions
    extensions = ["breathe"]

    # Breathe configuration
    breathe_projects = {"ZestCode": "xml"}
    breathe_default_project = "ZestCode"
