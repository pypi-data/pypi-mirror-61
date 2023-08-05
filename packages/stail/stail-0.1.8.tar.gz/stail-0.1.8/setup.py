# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stail']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.11.14,<2.0.0',
 'click>=7.0,<8.0',
 'colorama>=0.4.3,<0.5.0',
 'pyfiglet>=0.8.post1,<0.9']

entry_points = \
{'console_scripts': ['stail = stail:main']}

setup_kwargs = {
    'name': 'stail',
    'version': '0.1.8',
    'description': 'CLI Tool to run and tail a step function synchronously.',
    'long_description': '# Stail\nCLI Tool to run and tail a step function synchronously and persist event logs for the state machine execution on disk.\n\n![Screenshot](https://raw.githubusercontent.com/imankamyabi/stail/master/images/console-screenshot.png)\n\n\n## Installation:\n```shell\npip install stail\n```\n\n## Usage\n\n### run\nStarts a step function execution synchronously, tails the event history to the console and create a log file with all the events for the execution.\n\nLog file is stored at stail_logs/[execution name (UUID)].log \n\n```shell\nstail run --arn [state machine arn] --input [input]\n```\n####Options:\n  --arn  State machine ARN\n  --input Input JSON to the state machine\n\n##### Example:\n```shell\nstail run --arn arn:aws:states:<region>:955883056721:stateMachine:<name> --input "{\\"param\\":\\"hello\\"}"\n```\n\n### version\nDisplays the version.\n```shell\nstail version\n```\n\nAuthor: Iman Kamyabi\n \nFeedback: contact@imankamyabi.com',
    'author': 'Iman Kamyabi',
    'author_email': 'contact@imankamyabi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imankamyabi/stail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
