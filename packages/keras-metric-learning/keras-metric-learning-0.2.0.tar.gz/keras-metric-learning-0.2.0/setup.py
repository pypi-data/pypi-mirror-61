# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras-metric-learning']

package_data = \
{'': ['*']}

install_requires = \
['attrdict>=2.0.1,<3.0.0',
 'boto3>=1.10.44,<2.0.0',
 'boto>=2.49.0,<3.0.0',
 'cifar2png>=0.0.4,<0.0.5',
 'click>=7.0,<8.0',
 'hyperdash>=0.15.3,<0.16.0',
 'loguru>=0.4.0,<0.5.0',
 'opencv-python>=4.1.2,<5.0.0',
 'pandas>=0.25.3,<0.26.0',
 'pillow>=6.2.1,<7.0.0',
 'plot_keras_history>=1.1.19,<2.0.0',
 'py3nvml>=0.2.5,<0.3.0',
 'scikit-image>=0.16.2,<0.17.0',
 'scikit-learn>=0.22.1,<0.23.0',
 'seaborn>=0.9.0,<0.10.0',
 'split_folders>=0.3.1,<0.4.0',
 'streamlit>=0.53.0,<0.54.0',
 'tensorflow==2.1.0',
 'tqdm>=4.41.1,<5.0.0']

entry_points = \
{'console_scripts': ['train = train:run']}

setup_kwargs = {
    'name': 'keras-metric-learning',
    'version': '0.2.0',
    'description': 'Deep metric learning in tf2 keras',
    'long_description': '# keras-metric-learning',
    'author': 'Soumendra Dhanee',
    'author_email': 'soumendra@gmail.com',
    'maintainer': 'Soumendra Dhanee',
    'maintainer_email': 'soumendra@gmail.com',
    'url': 'https://github.com/soumendra/keras-metric-learning',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.5,<4.0.0',
}


setup(**setup_kwargs)
