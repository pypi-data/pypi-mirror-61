# setup_scmversion

Builds a pythonic version number based on information available on your scm (tag, branch, and number of commits).

See [LICENSE](LICENSE) for important licensing information.


## Instalation

Your `setup.py` will need `jfaleiro.setup_scmversion` to start - so you either make sure you have it pre-installed using pip:

```bash
pip install jfaleiro.setup-scmversion
```

## Use

A pythonic version number is created from standard data available in your *scm*, i.e. tag, branch name, and number of differences from master.

### Simplest Use

Should apply to most projects. Assumes your project has one main package. For this example let's name this package `mypackage`.  After installation add this to your `setup.py`:

```python
import mypackage
...
setup( ...
   version=mypackage.__version__),
   ...
)
```

Add this to your `mypackage.py` or `mypackage.__init__.py`:

```python
from ._version import __version__
```

Done. Now you just have to make sure you execute `scmversion tag-version` after installation and before any `setuptools` task that requires a version:

```bash
scmversion tag-version
...
python setup.py sdist # or any other command that requires a tagged version 
```

Examples of other possible setup commands are `develop`, `install`, `bdist`, and others.

To know usage details refer to `scmversion --help`


### Way More Complicated 

Add this on the very top of your `setup.py` and forget about it moving forward.

```python
try:
    import setup_scmversion
except ModuleNotFoundError as e:
    from pip._internal import main
    assert main('install jfaleiro.setup-scmversion'.split()) == 0
    
from setup_scmversion import version
```

Add these parameters to your `version` and `setup_requires` parameters in `setup.py`:

```python
setup(
    version=version(),
	...
    setup_requires=['jfaleiro.setup-scmversion'],
	...
)
```

## Versioning Schema

Release tags `release/<version>` with `nnn` differences from master will produce version `<version>.dev<nnn>` and a tagged version `<tag>` on master will produce the version `<tag>`. Everything else will produce `master.dev<nnn>` for master or `no-version.dev<nnn>` for any other branch. 

You can also use a command line based shortcut to peek at the current version:

```bash
jfaleiro@itacoatiara:~/gitrepos/setup_scmversion (release/0.0.1 *+)$ scmversion version
0.0.1.dev1
```

or the type of version, i.e.:

```bash
jfaleiro@itacoatiara:~/gitrepos/setup_scmversion (release/0.0.1 *+)$ scmversion version-type
RELEASE_BRANCH
```

The type of release can be one of `RELEASE`, `RELEASE_BRANCH`, `FEATURE_BRANCH`, or `OTHER`