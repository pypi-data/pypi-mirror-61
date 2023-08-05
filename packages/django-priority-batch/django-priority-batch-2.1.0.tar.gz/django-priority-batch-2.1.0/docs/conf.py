import os.path

# Get package metadata from '__about__.py' file.
about = {}
base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
with open(
    os.path.join(base_dir, 'src', 'django_priority_batch', '__about__.py'), 'r'
) as fh:
    exec(fh.read(), about)
if '__version__' not in about:
    raise AttributeError(
        "Package's version is not defined. Please, install the package."
    )

# -- General configuration ------------------------------------------------

# The extension modules to enable.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Django Priority Batch'
version = about['__version__']
release = version
author = about['__author__']
copyright = about['__copyright__']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Warn about all references where the target cannot be found.
nitpicky = True
# Except for the following:
nitpick_ignore = [
    # This is needed to prevent warnings for container types, e.g.:
    # :type foo: tuple(bool, str).
    ('py:obj', '')
]

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Output file base name for HTML help builder.
htmlhelp_basename = 'DjangoPriorityBatchdoc'

# Configuration for intersphinx.
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
