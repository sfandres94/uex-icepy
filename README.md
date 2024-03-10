<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]

# UEx-IcePy
This repository has been created for the ZeroC Ice lab session of the Distributed Computing subject at the University of Extremadura (UEx).

## Table of contents
* [Getting started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Usage](#usage)
* [Code examples](#code-examples)
* [License](#license)

## Getting started
The instructions below help you replicate this repository.

### Prerequisites
Anaconda distribution is recommended. You can install it following the [official installation guide](https://docs.anaconda.com/anaconda/install/linux/).

Check if Anaconda is installed (`--version`):
```
conda -V
```

### Installation
The file [environment.yml](environment.yml) contains all the necessary packages to use this project inside the environment provided with the name `icepy`. You can create a conda environment from the .yml file as follows (`--file`):
```
conda env create -f environment.yml
```

### Usage
Activate the conda environment:
```
conda activate ice
```

Compile the Slice definition to generate Python proxies and skeletons:
```
slice2py Printer.ice
```

Run the server in another terminal or hardware. Then, run the client.

## Code examples
The examples are organized in folders:
* [00_printer](00_printer) contains an example (based on the one given [here][ice-hello-world]) where the client sends to the server a message to be 'printed' via terminal.
* [CD22_23-P04_basic_calculator](CD22_23-P04_basic_calculator) is the solution to the first lab exercise where the client sends two values to a single server (the calculator) which does all the operations and returns the result.
* [CD22_23-P05_1_calculator_pro](CD22_23-P05_1_calculator_pro) is the solution to the second lab exercise. The client receives the IP addresses and ports of the servers via the terminal. One server performs addition and subtraction and the other division and multiplication, each returning the result to the client.
* [CD22_23-P05_2_bank](CD22_23-P05_2_bank) as an example of a simulation of a real-life problem or situation. It requires the compilers `slice2py` (currently under the Anaconda environment) and `slice2cpp` (installations details can be found [here][ice-cpp]). Makefile included. Only localhost.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://linkedin.com/in/sfandres
[ice-hello-world]: https://doc.zeroc.com/ice/3.7/hello-world-application/writing-an-ice-application-with-python
[ice-cpp]: https://zeroc.com/downloads/ice/3.7/cpp
