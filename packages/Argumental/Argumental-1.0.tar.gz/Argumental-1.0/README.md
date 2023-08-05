# Argumental

annotation descripters to put closuer on classes and objects to allow argparse to be easy to use

## Argue.py

A tool to decorate a python class to create an argparse ready command line application

Here is an example application

```python
#!/usr/bin/env python

import os,re,sys,json

from Argumental.Argue import Argue

args = Argue()

#====================================================================================================
@args.function(short='v', flag=True)
def verbose(): return False

#====================================================================================================
@args.command(single=True)
class ForTheSake(object):

    #________________________________________________________________________________________________
    @args.function(flag=True)
    def myFlag(self):
        '''
        this is a flag true if exists false if not
        '''
        return False

    #________________________________________________________________________________________________
    @args.function(choices=['a','b'])
    def myChoice(self):
        '''
        select for a list of choices,
        test if in or out of list
        '''
        return None

    #________________________________________________________________________________________________
    @args.function(short='n', type=int)
    def myNumber(self):
        '''
        this should expect an number of type int 
        '''
        return 0

    #________________________________________________________________________________________________
    @args.operation
    def myMethod(self, p1, p2, p3='d3', p4='d4'):
        '''
        this should be called myMethod
        and is a good example

        :param p1: p1 should be expected
        :type p1: str
        :param p2: p2 should be expected
        :type p2: int
        :param p3: p3 is optional use --p3 and defaults to d3
        :param p4: p3 is optional use --p4 and defaults to d4
        :return: json view of all variables
        :rtype: dict

        :Example:

        $ ./forTheSake.py [--] <command> <operation> <parameters> [--parameter=optional]

        '''
        return {
            'verbose' :  verbose(),
            'flag' :     self.myFlag(),
            'choice' :   self.myChoice(),
            'number' :   self.myNumber(),
            'p1' :       p1,
            'p2' :       p2,
            'p3' :       p3,
            'p4' :       p4
        }
        
#====================================================================================================
if __name__ == '__main__':
    print json.dumps(args.execute(), indent=4)
```


A sample usage would look like;

```bash
$ ./ofTheEngagement.py -h
usage: ofTheEngagement.py [-h] [--args] [-n MYNUMBER] [--myChoice {a,b}] [--myFlag] [-v]
                          {OfTheEngagment} ...

positional arguments:
  {OfTheEngagment}
    OfTheEngagment

optional arguments:
  -h, --help            show this help message and exit
  --args                show this argument tree
  -n MYNUMBER, --myNumber MYNUMBER
                        <type 'int'> this should expect an number of type int
  --myChoice {a,b}      select for a list of choices, test if in or out of list
  --myFlag              this is a flag true if exists false if not
  -v, --verbose
```


```bash
$ ./ofTheEngagement.py OfTheEngagment -h
usage: ofTheEngagement.py OfTheEngagment [-h] {myMethod} ...

positional arguments:
  {myMethod}
    myMethod  this should be called myMethod and is a good example

optional arguments:
  -h, --help  show this help message and exit

```

```bash
$ ./ofTheEngagement.py OfTheEngagment myMethod -h
usage: ofTheEngagement.py OfTheEngagment myMethod [-h] [--p3 P3] [--p4 P4] p1 p2

positional arguments:
  p1          <type 'str'> p1 should be expected
  p2          <type 'int'> p2 should be expected

optional arguments:
  -h, --help  show this help message and exit
  --p3 P3     <type 'str'> p3 is optional use --p3 and defaults to d3
  --p4 P4     <type 'str'> p3 is optional use --p4 and defaults to d4
```

```bash
$ ./ofTheEngagement.py -v --myFlag OfTheEngagment myMethod 1 2 --p3=3
{
    "p2": 2, 
    "p3": "3", 
    "flag": true, 
    "p1": "1", 
    "verbose": true, 
    "p4": "d4", 
    "number": 0, 
    "choice": null
}
```



