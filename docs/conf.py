import subprocess, os

# Run Doxygen to generate XML before building Sphinx docs
subprocess.call('doxygen', shell=True)

# Sphinx extensions
extensions = ["breathe"]

# Breathe configuration
breathe_projects = {"ZestCode": "xml"}
breathe_default_project = "ZestCode"
