def _is_root():
    """Checks if the user is rooted."""
    import os
    import ctypes
    try:
        return os.geteuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    return False


def cmdclass(path, enable=None, user=None):
    """Build nbextension cmdclass dict for the setuptools.setup method.

    Parameters
    ----------
    path: str
        Directory relative to the setup file that the nbextension code
        lives in.
    enable: [str=None]
        Extension to "enable".  Enabling an extension causes it to be loaded
        automatically by the IPython notebook.
    user: [bool=None]
        Whether or not the nbextension should be installed in user mode.
        If this is undefined, the script will install as user mode IF the
        installer is not sudo.

    Usage
    -----
    For automatic loading:
    # Assuming `./extension` is the relative path to the JS files and
    # `./extension/main.js` is the file that you want automatically loaded.
    setup(
        name='extension',
        ...
        cmdclass=cmdclass('extension', 'extension/main'),
    )

    For manual loading:
    # Assuming `./extension` is the relative path to the JS files.
    setup(
        name='extension',
        ...
        cmdclass=cmdclass('extension'),
    )
    """
    import warnings
    from setuptools.command.install import install
    from setuptools.command.develop import develop
    from os.path import dirname, join, exists, realpath
    from traceback import extract_stack

    try:
        # IPython/Jupyter 4.0
        from notebook.nbextensions import install_nbextension
        from notebook.services.config import ConfigManager
    except ImportError:
        # Pre-schism
        try:
            from IPython.html.nbextensions import install_nbextension
            from IPython.html.services.config import ConfigManager
        except ImportError:
            warnings.warn("No jupyter notebook found in your environment. "
                          "Hence jupyter nbextensions were not installed. "
                          "If you would like to have them,"
                          "please issue 'pip install jupyter'.")
            return {}

    # Check if the user flag was set.
    if user is None:
        user = not _is_root()

    # Get the path of the extension
    calling_file = extract_stack()[-2][0]
    fullpath = realpath(calling_file)
    if not exists(fullpath):
        raise Exception('Could not find path of setup file.')
    extension_dir = join(dirname(fullpath), path)

    # Installs the nbextension
    def run_nbextension_install(develop):
        import sys
        sysprefix = hasattr(sys, 'real_prefix')
        if sysprefix:
            install_nbextension(
                extension_dir, symlink=develop, sys_prefix=sysprefix)
        else:
            install_nbextension(extension_dir, symlink=develop, user=user)
        if enable is not None:
            print("Enabling the extension ...")
            cm = ConfigManager()
            cm.update('notebook', {"load_extensions": {enable: True}})

    # Command used for standard installs
    class InstallCommand(install):
        def run(self):
            print("Installing Python module...")
            install.run(self)
            print("Installing nbextension ...")
            run_nbextension_install(False)

    # Command used for development installs (symlinks the JS)
    class DevelopCommand(develop):
        def run(self):
            print("Installing Python module...")
            develop.run(self)
            print("Installing nbextension ...")
            run_nbextension_install(True)

    return {
        'install': InstallCommand,
        'develop': DevelopCommand,
    }
