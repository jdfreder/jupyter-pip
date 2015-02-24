# ipython-pip
Allows IPython notebook extension writers to make their extension pip installable!

Specifically, if you have a module that you've written which is intended for use in the IPython notebook and also has Javascript associated with it, this is designed to solve the distribution problem.

## Copy&paste
In setup.py

```python
try:
    from ipythonpip import cmdclass
except:
    cmdclass = lambda *args: None
```

and inside the `setup(...)` call

```python
    install_requires=["ipython-pip"],
    cmdclass=cmdclass('myplugin', 'myplugin/init'),
```

## Details
You **don't** need to download this to use it!  Instead you just need to modify your package's `setup.py` to download it at install time.

The following example assumes a folder structure like this:
```
./myplugin/__init__.py
./myplugin/init.js
./setup.py
```

Starting with a setup.py file that looks like this:
```python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='myplugin',
    packages=['myplugin'],
    # ... more setup.py stuff here ...
)
```

All you need to do is add a try import block and two entries to the setup call to make the project nbextension compatabile:
```python
# -*- coding: utf-8 -*-
from setuptools import setup

try:
    from ipythonpip import cmdclass
except:
    cmdclass = lambda *args: None

setup(
    name='myplugin',
    packages=['myplugin'],
    # ... more setup.py stuff here ...
    install_requires=["ipython-pip"],
    cmdclass=cmdclass('myplugin', 'myplugin/init'),
)
```

The second argument to the `cmdclass` call is optional.  If specified, the JS module will be loaded alongside the notebook automatically.  **Note that for widget packages, typically this isn't this best idea.  Instead the line would read `cmdclass=cmdclass('myplugin')` and the widget framework would load the JS when the widget is constructed.**


## License
New BSD (see `./LICENSE` file).
