# conan-qplot
A Conan package for qplot

## Updating the conan package

1. Edit line 7 of the *conanfile.py*-file to set the commit tag of the new conan package.

2. When in the directory of the local copy of *conan-qplot*, execute this command:

	```
	conan create . qplot/xxxxxx@ess-dmsc/stable
	```
	Where **xxxxxx** is the hash of the used commit as set in the file *conanfile.py*.

4. Upload the new package to the relevant conan package repository by executing:

	```
	conan upload qplot/xxxxxx@ess-dmsc/stable --remote alias_of_repository
	```
