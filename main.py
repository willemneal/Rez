import os
import tempfile
import numpy as np
import json, pickle
INPUT_FILE = ".inputs.rez"
class Rez(object):
    inputs = {}

    @classmethod
    def add(cls,numpy=True):
        if not os.path.isfile(INPUT_FILE):
            with open(INPUT_FILE,'w+')as _file:
                pickle.dump(cls.inputs,_file)
        elif len(cls.inputs) == 0:
            with open(INPUT_FILE,'r') as _file:
                cls.inputs = pickle.load(_file)
        def wrapf(f):
            fName = f.func_name
            def res(*args,**kwargs):
                fileName = ".{}.rez".format(fName)
                _input = [args, kwargs]

                if fName not in cls.inputs:
                    with open(fileName,'w+')as _file:
                        cls.updateInputs(fName,_input)
                        json.dump(f(*args,**kwargs),_file)

                print "f in cls.input", cls.inputs[fName]== _input
                read = cls.inputs[fName] == _input
                print read
                with open(fileName, 'rw+') as _file:
                    if read:
                        if numpy:
                            output = np.load(_file)
                        else:
                            output = json.load(_file)

                    else:
                        output = f(*args, **kwargs)
                        if numpy:
                            np.save(_file, output)
                        else:
                            json.dump(output,_file)
                return output

            return res
        return wrapf

    @classmethod
    def updateInputs(cls,fName,_input):
        cls.inputs[fName] = _input
        print cls.inputs[fName]
        print cls.inputs
        with open(INPUT_FILE,'w+') as _file:
            pickle.dump(cls.inputs,_file)

@Rez.add(numpy=False)
def foo(x):
    return 5

print foo(3)
print foo(3)
