from setuptools import setup

setup(
    name='CommandCompiler',
    version='0.1.0',
    author='Steven Kellum',
    author_email='sk@perfectatrifecta.com',
    description='CommandCompiler is a Python library for executing shell commands with enhanced features.',
    download_url='https://github.com/RI7TE/CommandCompiler.git',
    license="'Proprietary License'",
    packages=[],
    py_modules=['command'],
    python_requires=">={}.{}".format(3, 13),
    install_requires=['colorama==0.4.6'],

)
