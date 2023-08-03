# setdata.py
import subprocess


def send_csv_data_to_influx(csv_file, influxdb_host, influxdb_port, token, organization, bucket):
    header1 = '#constant measurement,kuku'
    header2 = '#datatype dateTime:2006-01-02,long,tag'
    command = f'D:/influxdb2-client-2.7.3-windows-amd64/influx write -b {bucket} -o {organization} -t {token} -f {csv_file} --host http://{influxdb_host}:{influxdb_port} --header "{header1}" --header "{header2}"'
    subprocess.run(command, shell=True)


# Example usage
csv_file = 'D:\example.csv'
influxdb_host = 'localhost'
influxdb_port = '8086'
token = 'sQY1wYw3yDcRg35YExT3GD9PCn_EPZOBW5hlNIdq5vVbK4VG4mGdv4sEqU6PtPfiQwBa2AIt6cin0VlrX4jNxQ=='
organization = '51210a7db2211551'
bucket = 'sample'

send_csv_data_to_influx(csv_file, influxdb_host,
                        influxdb_port, token, organization, bucket)
