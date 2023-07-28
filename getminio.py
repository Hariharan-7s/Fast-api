import minio
import io
from setinflux import perform_insertdata
minio_client = minio.Minio('play.min.io',
                           'WWT243vlCzx24DlcGKxJ', '4RQoYZ2E2SSo6XeYGchftXEucp5NDqX8lKc4erxk', secure=True)


def download_object(bucket_name, object_name):

    response = minio_client.get_object(bucket_name, object_name,)

# Read the content of the CSV file as a file-like object
    csv_file_object = io.BytesIO(response.data)

# Now, csv_file_object contains the CSV file as a file-like object
# You can work with this object directly

# For example, you can print the content of the CSV file:
    file_path = csv_file_object.read().decode('utf-8')
    perform_insertdata(file_path)
