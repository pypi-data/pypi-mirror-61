from enum import Enum

class Level(Enum):
    RESET = 0
    INFO = 1
    SUCCESS = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

colors = {
    Level.RESET: '\033[0m',
    Level.INFO: '\033[34m',
    Level.SUCCESS: '\033[32m',
    Level.WARNING: '\033[93m',
    Level.ERROR: '\033[91m',
    Level.CRITICAL: '\033[31m',
}

icons = {
    Level.INFO: 'i',
    Level.SUCCESS: '\u2713',
    Level.WARNING: '!',
    Level.ERROR: 'x',
    Level.CRITICAL: '\u26A0',
}

def message(level, text):
    out = '['
    out += colors[level]
    out += icons[level]
    out += colors[Level.RESET]
    out += '] '
    out += text
    return out

def sprint(level, text):
    print(message(level, text))
