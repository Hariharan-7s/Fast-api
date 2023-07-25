import minio
from setinflux import perform_insertdata
minio_client = minio.Minio('play.min.io',
                           'WWT243vlCzx24DlcGKxJ', '4RQoYZ2E2SSo6XeYGchftXEucp5NDqX8lKc4erxk')


def download_object(bucket_name, object_name, local_file_path):
    chunk_size = 512 * 1024  # 512 KB chunk size
    with open(local_file_path, 'wb') as csvfile:
        data = minio_client.get_object(bucket_name, object_name)
        for line in data.stream(chunk_size):
            csvfile.write(line)

    """
    csv_url = minio_client.presigned_get_object(bucket_name, object_name)
    perform_insertdata(file_path=csv_url) 
    """


"""Downloads an object from the MinIO server to a local file.

    Args:
        bucket_name (str): The name of the bucket.
        object_name (str): The name of the object.
        local_file_path (str): The path to the local file.
    """

# This code used for download file locally
