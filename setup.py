from setuptools import setup, find_packages
from functools import partial
from os import path
from pip import __file__ as pip_loc


if __name__ == '__main__':
    package_name = 'bettertutors_oss'

    config_join = partial(path.join, path.dirname(__file__),
                          package_name, 'config')
    install_to = path.join(path.split(path.split(pip_loc)[0])[0],
                           package_name, 'config')

    setup(
        name=package_name,
        author='Samuel Marks',
        version='0.13.2',
        test_suite=package_name + '.tests',
        packages=find_packages(),
        package_dir={package_name: package_name},
        data_files=[(install_to, [config_join('strategy.sample.json')])]
    )
