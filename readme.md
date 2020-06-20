# Purpose:
This tool will primarily parse out git operations and graph them for statistics tracking of an environment, in a hour by hour basis, based on the application-logs/atlassian-bitbucket-access* logs found within a Bitbucket Support zip.

# Usage:
Run the "pylogparser.py" file pointed at the "application-logs" directory from a Bitbucket support zip to build several graphs on the usage statistics of the environment.

        python3 plugin-checker.py -p /path/to/application-logs

You can also pass a directory which contains multiple support zips and the tool will then name each pdf created based on the folder directory naming. For Example, if you were to use the path:

        python3 plugin-checker.py -f /home/<user-name>/Downloads/multi-nodes
    
Where "multi-nodes" is a directory containing...
 - Node 1 - application-config - bitbucket.properties
          \ application-logs - *.logs
          \ application-properties - application.xml
 - Node 2 - application-config - bitbucket.properties
          \ application-logs - *.logs
          \ application-properties - application.xml

Then 2 pdfs will be created, one named "Node 1" another named "Node 2" (whatever the folder names are)

# Dependencies:
* [Python3](https://www.python.org/downloads/) This was written in python3.7 and requires at least 3.5+ to operate as expected.
* [matplotlib](https://matplotlib.org/)

        pip3 install matplotlib --user

* [img2pdf](https://pypi.org/project/colorama/)

        pip3 install img2pdf --user


Or Install all dependencies at once via the requirements.txt file

        pip3 install -r requirements.txt --user
