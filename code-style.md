# Code Style

To have a common code style, here is some cheat sheet to follow. Generally we want to:
- Use CamelCase names for functions, variables, classes and their methods
  - Class names should be Capitalized
  - functions, methods and variables should be lower case.
- Constants are written all CAPITAL and with underscores to separate words

Have some example code:
```
NEVER_CHANGING_CONSTANT_NAME = 3.1415926535
    
def lowerCaseFunctionName():
    pass
        
lowerCaseVariableName = True
    
class CapitalClassName:
    lowerCaseStaticVariable = 'some class specific value'
      
    def lowerCaseMethodName(self):
        pass
```

## Naming files and packages (folders)

For naming files and packages (folders), here are some rules:
- no hyphens (-)
- also camelCased
  - does the file only contain one class then it shall be
    - Capitalized
    - named after the class it is containing
    - other smaller supplementary classes in that same file are allowed and wanted especially when the supplementary class only makes sense to be handled by the main class of the file.
  - in case the file just contains some code it shall be lowerCased

Have some examples:
```
# ClassFile.py
 
class ClassFile:
    someOtherClassOnlyIUse = SupplementaryClass()

class SupplementaryClass:
    pass
    
