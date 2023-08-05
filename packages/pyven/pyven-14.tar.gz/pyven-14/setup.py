import setuptools

def long_description():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
        name = 'pyven',
        version = '14',
        description = 'Management of PYTHONPATH for simultaneous dev of multiple projects',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/pyven',
        author = 'Andrzej Cichocki',
        packages = setuptools.find_packages(),
        py_modules = ['pyven', 'gclean', 'tasks', 'initopt', 'travis_ci', 'tests', 'release', 'runtests'],
        install_requires = ['twine', 'aridity'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        scripts = ['foreignsyms'],
        entry_points = {'console_scripts': ['gclean=gclean:main_gclean', 'initopt=initopt:main_initopt', 'pyven=pyven:main_pyven', 'release=release:main_release', 'tests=runtests:main_tests', 'tasks=tasks:main_tasks', 'travis_ci=travis_ci:main_travis_ci']})
