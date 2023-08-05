# Platea

Platea is a passion project of mine. While working to optimize code for my day job as a Data Scientist, I began exploring the wonderful worlds of C++ and Fortran. I became very interested in learning how to implement numerical methods at a low level and in a performant manner. This code is a product of that work.

I'm open to all questions, feedback, commentary, and suggestions as long as they are constructive and polite! Discussions should always come in the form of git issues. 

One of the big design philosophy differences between this package and packages like numpy is that this package is not made to be fool proof. For example, there are functions where we assume that users will read the docs and input appropriate arguments. We have intentionally left out assertions to check if these arguments conform to the docs. This reduces run times, but it also removes a safety net that many python users rely on.

### Authors

**James Montgomery** - *Initial work* - [jamesmontgomery.us](http://jamesmontgomery.us)

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### The name Platea

Why name a statistics package Platea? In addition to being a stats nerd I am also a history wonk. When writing this package I was reminded of a story in Thucydides' "History of the Peloponnesian War" where the Athenians needed to estimate the height of the walls surrounding Platea in order to know how high to make their siege ladders. The Athenians counted the number of bricks at a number of unplastered sections of wall and used the mode of these counts and the estimated height of a brick to approximate the height of the walls. This is one of the earliest recorded applications of "statistics" (5th Century BC).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

For a local installation, first git clone this repository. Then follow these instructions:

```
pip install .
```

To install from pypi:

```
pip install -U platea
```

## Testing

Testing is an important part of creating maintainable, production grade code. Below are instructions for running unit and style tests as well as installing the necessary testing packages. Tests have intentionally been separated from the installable pypi package for a variety of reasons.

Make sure you have the required testing packages:

```
pip install -r requirements_test.txt
```

You will also need to build the package extensions in place:

```
python setup.py build_ext --inplace
```

### Running the unit tests

We use the pytest framework for unit testing.

```
pytest -vvl -s --cov platea --disable-pytest-warnings
```

### Running the style tests

Having neat and legible code is important. Having documentation is also important. We use pylint as our style guide framework. Many of our naming conventions follow directly from the literary sources they come from. This makes it easier to read the mathematical equations and see how they translate into the code. This sometimes forces us to break pep8 conventions for naming.

```
pylint platea --disable=invalid-name
```

## Acknowledgments

A big thank you to Keegan Hines who first recommended the book "Numerical Recipes" to me. Another big thank you to Mack Sweeney who has shaped much of my appreciation for code styling and standards. Finally, thanks to Greg Sinclair for being a sounding board and source of advice as I worked on this package.

## Literary References

Book References:
1. [Numerical Recipes in Fortran Second Edition](https://websites.pmc.ucsc.edu/~fnimmo/eart290c_17/NumericalRecipesinF77.pdf)
2. [Numerical Recipes in Fortran 90 Second Edition](http://www.elch.chem.msu.ru/tch/group/FortranBooks/NumericalRecipesinF90.pdf)
3. [Numerical Recipes in C Second Edition](https://www.cec.uchile.cl/cinetica/pcordero/MC_libros/NumericalRecipesinC.pdf)
3. [Numerical Recipes in C Third Edition]()
