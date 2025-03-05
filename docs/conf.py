import subprocess, os

project = "ZestCode"
# html_theme = "sphinx_rtd_theme"
html_theme = "sphinx_immaterial"
# Run Doxygen to generate XML before building Sphinx docs
subprocess.call('doxygen', shell=True)


# Sphinx extensions
extensions = ["breathe", "m2r2", "sphinx_immaterial"]

# Breathe configuration
breathe_projects = {"ZestCode": "xml"}
breathe_default_project = "ZestCode"
