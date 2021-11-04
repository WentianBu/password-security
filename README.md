# Password Security - UCAS
This is the project of the UCAS Web Security Course. In this project, we analyze the structure of the leaked passwords from CSDN and Yahoo, including length, keyboard patterns, date patterns and words. We also design a program using PCFG (Probabilistic Context Free Grammar) to learn the probabilities from the passwords, generate the attack dictionary and test a dictionary on a password set.

## File Structure

 `analysis` contains the programs and the results of the analysis of passwords, including date pattern analysis, keyboard pattern analysis, length analysis and word analysis.

`generate` contains the programs to generate attack dictionary, as well as the data and results of the program. `main.py` is the entrance of the program.

## Prerequisites

python 3.8

python libraries: 

- tqdm: display progress bar
- prettytable: display pretty table

## Generate

This program uses PCFG to generate an attack dictionary. We make it a python module `pcfg`,  including `pcfg.data` and `pcfg.model`. The program is well designed and encapsulated, so you can use it in several simple statements. We also provide a entrance with sound help information, so you can easily run it as a command line program.

### Command Line Usage

`main.py [-h] [-d {csdn,yahoo}] [-o OUTPUT] [-l LENGTH] [-p PWDICT] {train,gen,test} infile`

#### Important parameters description:

`-h/--help`: show the help information

`train/gen/test`: specify the function of the program

#### Learn the model parameters from a password set

`main.py train -d csdn/yahoo -o xxx.model xxx_password.txt`

You must specify the type of dataset (csdn or yahoo). Only support the origin format.

#### Generate attack dictionary from a model

`main.py gen -l 5000 -o xxx.dict xxx.model`

If you don't specify the length of the dictionary, the default length is 5000. Note: longer dictionary will cost much more time.

#### Test a dictionary on a password set

`main.py test -d csdn/yahoo -p xxx.dict xxxx_password.txt`

You must specify the type of the password set (csdn or yahoo). Test may be slow, because python only use one CPU core. You will get a brief statistic of the result.

### Programming Usage

We provide some classes and methods, so you can easily write a python script to use the module.

#### Load password set

We design two classes in `pcfg.data` for csdn format and yahoo format. The two classes return an iterator.

```python
import pcfg.data
csdn = pcfg.data.CSDN('path_to_csdn_pwds.txt')
yahoo = pcfg.data.Yahoo('path_to_yahoo_pwds.txt')
```

#### Train a model and export

We design a `Model` class in `pcfg.model`. It is very easy to use.

```python
import pcfg.data
import pcfg.model
csdn = pcfg.data.CSDN('path_to_csdn_pwds.txt')
m = pcfg.model.Model()
m.fit(csdn) # train
m.export('csdn.model') # export as a file
```

#### Generate a dictionary

You need a model before generating. It can be loaded from a model file, or trained from a password set.

```python
import pcfg.model
m = pcfg.model.load_model('csdn.model')
m.generate('csdn.dict', 5000) # 5000 is optional
```

#### Test a dictionary

You need to load the dictionary and the password set before test. We provide a class `Pwdlist` in `pcfg.data` to load a dictionary.

```python
import pcfg.data
d = pcfg.data.Pwdlist('csdn.dict')
csdn = pcfg.data.CSDN('path_to_csdn_pwds.txt')
d.test(csdn)
```



