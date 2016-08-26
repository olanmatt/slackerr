from setuptools import setup

setup(
    name="slackerr",
    version="0.0.0",
    url="https://github.com/olanmatt/slackerr",
    author="Matt Olan",
    author_email="hello@olanmatt.com",
    description="Pipe directly to Slack from your shell",
    long_description=open('README.md').read(),
    py_modules=['slackerr'],
    entry_points={
        'console_scripts': ['slackerr = slackerr:slackerr']
    },
    install_requires=['slackclient']
)
