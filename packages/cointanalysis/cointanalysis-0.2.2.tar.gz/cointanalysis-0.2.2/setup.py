# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cointanalysis']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.0,<2.0.0', 'sklearn>=0.0,<0.1', 'statsmodels>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'cointanalysis',
    'version': '0.2.2',
    'description': 'Python package for cointegration analysis.',
    'long_description': '# CointAnalysis\n\n[![version](https://img.shields.io/pypi/v/cointanalysis.svg)](https://pypi.org/project/cointanalysis/)\n[![Build Status](https://travis-ci.com/simaki/cointanalysis.svg?branch=master)](https://travis-ci.com/simaki/cointanalysis)\n[![LICENSE](https://img.shields.io/github/license/simaki/cointanalysis)](LICENSE)\n\nPython library for cointegration analysis.\n\n![hyg-bkln-adjust](./examples/howto/hyg-bkln-adjust.png)\n\n## Features\n\n- Carry out cointegration test\n- Evaluate spread between cointegrated time-series\n- Generate cointegrated time-series artificially\n- Based on scikit-learn API\n\n## Installation\n\n```sh\n$ pip install cointanalysis\n```\n\n## What is cointegration?\n\nSee [Hamilton\'s book][hamilton].\n\n## How to use\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/simaki/cointanalysis/blob/master/examples/howto/howto.ipynb)\n\nLet us see how the main class `CointAnalysis` works using two ETFs, [HYG][hyg] and [BKLN][bkln], as examples.\nSince they are both connected with liabilities of low-rated companies, these prices behave quite similarly.\n\n![hyg-bkln](./examples/howto/hyg-bkln.png)\n\n### Cointegration test\n\nThe method `test` carries out a cointegration test.\nThe following code gives p-value for null-hypothesis that there is no cointegration.\n\n```python\nfrom cointanalysis import CointAnalysis\n\nhyg = ...   # Fetch historical price of high-yield bond ETF\nbkln = ...  # Fetch historical price of bank loan ETF\nX = np.array([hyg, bkln]).T\n\ncoint = CointAnalysis()\ncoint.test(X)\n\ncoint.pvalue_\n# 0.0055\n```\n\nThe test have rejected the null-hypothesis by p-value of 0.55%, which implies cointegration.\n\n[hyg]: https://www.bloomberg.com/quote/HYG:US\n[bkln]: https://www.bloomberg.com/quote/BKLN:US\n\n### Get spread\n\nThe method `fit` finds the cointegration equation.\n\n```python\ncoint = CointAnalysis().fit(X)\n\ncoint.coef_\n# np.array([-0.18  1.])\ncoint.mean_\n# 6.97\ncoint.std_\n# 0.15\n```\n\nThis means that spread "-0.18 HYG + BKLN" has the mean 6.97 and standard deviation 0.15.\n\nIn fact, the prices adjusted with these parameters clarifies the similarities of these ETFs:\n\n![hyg-bkln-adjust](./examples/howto/hyg-bkln-adjust.png)\n\nThe time-series of spread is obtained by applying the method `transform` subsequently.\nThe mean and the standard deviation are automatically adjusted (unless you pass parameters asking not to).\n\n```python\nspread = coint.transform(X)\n# returns (-0.18 * hyg + 1. * bkln - 7.00) / 0.15\n\nspread = coint.transform(X, adjust_mean=False, adjust_std=False)\n# returns -0.18 * hyg + 1. * bkln\n```\n\nThe method `fit_transform` carries out `fit` and `transform` at once.\n\n```python\nspread = coint.fit_transform(X)\n```\n\nThe result looks like this:\n\n![hyg-bkln-spread](./examples/howto/hyg-bkln-spread.png)\n\n## Acknowledgements\n\n- [statsmodels](https://www.statsmodels.org/)\n\n## References\n\n- [J. D. Hamilton, "Time Series Analysis", (1994)][hamilton].\n\n[hamilton]: https://press.princeton.edu/books/hardcover/9780691042893/time-series-analysis\n[statsmodels-aeg]: https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html\n',
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simaki/cointanalysis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
