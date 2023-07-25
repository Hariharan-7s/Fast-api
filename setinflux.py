import subprocess
from fastapi import Query


def perform_insertdata(file_path: str = Query(None)):
    header1 = '#constant measurement,newmin'
    header2 = '#datatype dateTime:2006-01-02,long,tag'
    command = f'D:/influxdb2-client-2.7.3-windows-amd64/influx write -b sample -o 51210a7db2211551 -t sQY1wYw3yDcRg35YExT3GD9PCn_EPZOBW5hlNIdq5vVbK4VG4mGdv4sEqU6PtPfiQwBa2AIt6cin0VlrX4jNxQ== -f {file_path} --host http://localhost:8086 --header "{header1}" --header "{header2}"'
    subprocess.run(command, shell=True)
    print('Everything OK!')
