# `linalg_for_datasci`

Code supporting the computational instruction for the course STAT 89A: Linear Algebra for Data Science at UC Berkeley.

## Contributing

[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)  


If the `pre-commit` Python package is installed, you can set up `pre-commit` hooks for automatic code formatting via

    pre-commit install

You can also invoke the pre-commit hook manually at any time with

    pre-commit run

Automatic code formatting has been adopted for `linalg_for_datasci` to make it unnecessary for contributors to worry about their code style.
As long as the code is valid, the pre-commit hook should take care of how the code should look.

There are also plugins to [integrate the `black` code autoformatter into your favorite code editor](https://github.com/psf/black#editor-integration). This way you can format code automatically.

If you have already committed files before setting up the pre-commit hook with `pre-commit install`, you can fix everything up using `pre-commit run --all-files`. You need to make the fixing commit yourself after that.
