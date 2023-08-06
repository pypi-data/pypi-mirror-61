# SageMaker Job Registry

This is a generic class that can be used to register your SageMaker jobs that is both train and, or serve by sub-classing the SageMakerRegistry class. 

The dockerized code automatically load code in /opt/program to register any classes that is sub-classed and use that in the `serve` and `train` method


