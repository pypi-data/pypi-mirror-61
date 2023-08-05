# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fn_graph_studio']

package_data = \
{'': ['*']}

install_requires = \
['dash-treebeard>=0.0.1,<0.0.2',
 'dash>=1.7,<2.0',
 'dash_core_components>=1.6,<2.0',
 'dash_interactive_graphviz>=0.1.0,<0.2.0',
 'dash_split_pane>=1.0,<2.0',
 'fn_graph>=0.1.5,<0.2.0',
 'pandas>=0.25.3,<0.26.0',
 'plotly>=4.4,<5.0']

setup_kwargs = {
    'name': 'fn-graph-studio',
    'version': '0.2.6',
    'description': 'A web based explorer for fn_graph function composers',
    'long_description': None,
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
