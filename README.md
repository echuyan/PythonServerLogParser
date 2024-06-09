# PythonServerLogParser
Practising server logs parsing

The script takes either a filename or directory as and argument of the "main" function.
The script is able to analyze the given file or all .log files in the given directory and print out the following stats:
    Total count of the requests made
    Requests count corresponding to HTTP methods: GET, POST, PUT, DELETE, OPTIONS, HEAD. Например, GET - 20, POST - 10 etc
    top 3 IP addressess that made the most of the requests
    топ 3 longest requests 

Those stats are also saved in the .json file that has a timestamp as a filename.
