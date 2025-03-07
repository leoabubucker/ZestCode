import subprocess, os

project = "ZestCode"
html_theme = "sphinx_rtd_theme"

# Sphinx extensions
extensions = ["breathe", "m2r2"]

# Run Doxygen to generate XML before building Sphinx docs
subprocess.call('doxygen', shell=True)


# Breathe configuration
breathe_projects = {"ZestCode": "xml"}
breathe_default_project = "ZestCode"

breathe_projects_source = {
    "common" : ("../include/common", [f for f in os.listdir("../include/common") if f.endswith(".h")])
}