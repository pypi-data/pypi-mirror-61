# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enchant', 'enchant.checker', 'enchant.tokenize']

package_data = \
{'': ['*'],
 'enchant': ['lib/enchant/*',
             'share/enchant/*',
             'share/enchant/ispell/*',
             'share/enchant/myspell/*']}

setup_kwargs = {
    'name': 'pyenchant',
    'version': '3.0.0rc1',
    'description': 'Python bindings for the Enchant spellchecking system',
    'long_description': 'Status: maintenance transfer\n-----------------------------\n\nMaintenance of this project is getting transferred from\nRyan Kelly to me, Dimitri Merejkowsky. Expect a few bumps\ndown the road while issues are sorted out.\n\nA new release is being worked on, see the `"next release" milestone <https://github.com/pyenchant/pyenchant/milestone/1>`_\nfor more details.\n\npyenchant:  Python bindings for the Enchant spellchecker\n========================================================\n\nThis package provides a set of Python language bindings for the Enchant\nspellchecking library.  For more information, visit the project website:\n\n    http://pyenchant.github.io/pyenchant/\n\nWhat is Enchant?\n----------------\n\nEnchant is used to check the spelling of words and suggest corrections\nfor words that are miss-spelled.  It can use many popular spellchecking\npackages to perform this task, including ispell, aspell and MySpell.  It\nis quite flexible at handling multiple dictionaries and multiple\nlanguages.\n\nMore information is available on the Enchant website:\n\n    http://www.abisource.com/enchant/\n\n\nHow do I use it?\n----------------\n\nFor Windows and OSX users, install the pre-built binary packages using\npip::\n\n    pip install pyenchant\n\n\nThese packages bundle a pre-built copy of the underlying enchant library.\nUsers on other platforms will need to install "enchant" using their system\npackage manager.\n\nOnce the software is installed, python\'s on-line help facilities can\nget you started.  Launch python and issue the following commands:\n\n    >>> import enchant\n    >>> help(enchant)\n\n\n\nWho is responsible for all this?\n--------------------------------\n\nThe credit for Enchant itself goes to Dom Lachowicz.  Find out more details\non the Enchant website listed above.  Full marks to Dom for producing such\na high-quality library.\n\nThe glue to pull Enchant into Python via ctypes was written by Ryan Kelly.\nHe needed a decent spellchecker for another project he was working on, and\nall the solutions turned up by Google were either extremely non-portable\n(e.g. opening a pipe to ispell) or had completely disappeared from the web\n(what happened to SnakeSpell?)  It was also a great excuse to teach himself\nabout SWIG, ctypes, and even a little bit of the Python/C API.\n\nFinally, after Ryan stepped down from the project, Dimitri Merejkowsky\nbecame the new maintainer.\n\n',
    'author': 'Dimitri Merejkowsky',
    'author_email': 'd.merej@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pyenchant.github.io/pyenchant/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
