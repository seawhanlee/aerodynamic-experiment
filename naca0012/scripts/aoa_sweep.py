from configparser import RawConfigParser
import sys


# Initiate ini
ini = RawConfigParser()
ini.optionxform = str

# read ini file from first argument
ini.read(sys.argv[1])

# Change aoa from second argument
ini.set('constants', 'aoa', sys.argv[2])

# Save as the file whose name is third argument
with open(sys.argv[3], 'w') as fp:
    ini.write(fp)
