import subprocess, os

project = "ZestCode"

# Sphinx extensions
extensions = ["breathe", "m2r2", "sphinx_immaterial"]
# html_theme = "sphinx_rtd_theme"
html_theme = "sphinx_immaterial"
# Run Doxygen to generate XML before building Sphinx docs
subprocess.call('doxygen', shell=True)


# Breathe configuration
breathe_projects = {"ZestCode": "xml"}
breathe_default_project = "ZestCode"
