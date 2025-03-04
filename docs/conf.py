import subprocess, os

project = "ZestCode"
html_theme = "sphinx_rtd_theme"
# Run Doxygen to generate XML before building Sphinx docs
subprocess.call('doxygen', shell=True)


# Convert XML to Sphinx .rst files
subprocess.call('doxygen2sphinx xml docs/api', shell=True)

# Sphinx extensions
extensions = ["breathe"]

# Breathe configuration
breathe_projects = {"ZestCode": "xml"}
breathe_default_project = "ZestCode"
