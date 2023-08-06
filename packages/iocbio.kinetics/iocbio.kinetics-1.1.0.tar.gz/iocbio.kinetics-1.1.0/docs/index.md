# Kinetics analysis program

IOCBIO Kinetics is a cross-platform application for analysis of different traces, as described by its plugins. While originally developed for analysis of enzyme kinetics, the other types of traces can be analyzed as well. It is designed to analyze traces where some measured parameter depends on one other parameter, such as time or space. For example, respiration rate measurements via following oxygen concentration in time and its changes induced through addition of metabolites.

<img src="img/screenshot.png">_Example analysis of respiration kinetics_


The analysis of experimental traces is built as a pipeline, with the data imported from the experiment file, regions of interest automatically generated or set by user, data fitted and analyzed. Communication between different plugins is done through the database backend with the analysis results stored in the database. Software is modular with the new modules added easily to fit the new types of experiments.

## Links

- [Project page](https://gitlab.com/iocbio/kinetics)
- [Issues](https://gitlab.com/iocbio/kinetics/issues)
- [Demos](https://www.youtube.com/channel/UCAyvqIEqVARCmtQ_5XQYJaQ/videos)
- [Example dataset](example-data/18-06-04_1_ch3.txt)

Please use the public issues when you want to get assistance with installation, reading your data, suggest extension or improvement of the software. By doing it openly, you can help others with the same problems or suggestions.

## Copyright

Copyright (C) 2018 [Laboratory of Systems
Biology](https://sysbio.ioc.ee), Department of Cybernetics, School of
Science, Tallinn University of Technology.

Software license: GPLv3.

Contact: Marko Vendelin <markov@sysbio.ioc.ee>
