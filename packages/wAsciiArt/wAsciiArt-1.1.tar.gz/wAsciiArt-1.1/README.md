# wAsciiArt

Simple python module providing witrdotnet in ASCII art

```
           _ _           _       _              _   
 __      _(_) |_ _ __ __| | ___ | |_ _ __   ___| |_ 
 \ \ /\ / / | __| '__/ _` |/ _ \| __| '_ \ / _ \ __|
  \ V  V /| | |_| | | (_| | (_) | |_| | | |  __/ |_ 
   \_/\_/ |_|\__|_|  \__,_|\___/ \__|_| |_|\___|\__|
                                                            
```

# Usage

```
pip install wAsciiArt
```

## With command line

```
python -m wAsciiArt
```

## With interactive interpreter

```
$ python
>>> from wAsciiArt import Waa
>>> w = Waa()
>>> print(w.getAsciiArt())
```

## In project

```
from wAsciiArt import Waa
  
waa = Waa()
print(waa.getAsciiArt())
```
