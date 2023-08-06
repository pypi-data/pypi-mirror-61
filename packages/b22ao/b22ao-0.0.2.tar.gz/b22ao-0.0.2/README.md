# b22ao: API for B22 adaptive optics operations

This package provides the basic API for Adaptive Optics scripts running at beamline B22 in Diamond Light Source.

Adaptive Optics operations must implement b22ao.base.BaseOperation, which provides methods for deforming mirrors and
capturing images. The implementation is run by the AO manager which will inject any given JSON configuration file.

Example:
```python
from b22ao.base import BaseOperation
import numpy

class MyAO(BaseOperation):
    def start(self):
        max_iter = self.config['max_iter']

        self.select_dm(self.config['mirror'])

        self.stopping = False
        for iter in range(max_iter):
            if self.stopping:
                self.stopping = False
                break
            self.deform(numpy.zeros(97))
            self.capture()
    
        print("Finished!")

    def stop(self):
        self.stopping = True
```
And the configuration file:
```json
{
  "max_iter": 300,
  "mirror": 2
}
```
