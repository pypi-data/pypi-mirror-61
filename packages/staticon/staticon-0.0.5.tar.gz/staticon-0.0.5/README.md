# Staticon
A python library for printing pretty status messages
## Installation
`pip install --user staticon`
## Usage
`message` returns the text to print  
`sprint` calls `message` and prints the output
#### Source
```python
from staticon import Level, sprint

sprint(Level.INFO, 'This is the info level')
sprint(Level.SUCCESS, 'This is the success level')
sprint(Level.WARNING, 'This is the warning level')
sprint(Level.ERROR, 'This is the error level')
sprint(Level.CRITICAL, 'This is the critical level')
```
#### Output
It displays
```
[i] This is info
[✓] This is success
[!] This is warning
[x] This is error
[⚠] This is critical
```