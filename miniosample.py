import io
import minio

# Create a Minio client
minio_client = minio.Minio('play.min.io',
                           'minioadmin', 'minioadmin', secure=True)


def download_object(bucket_name, object_name):
    data = minio_client.get_object(bucket_name, object_name)
    csv_data = io.StringIO(data.data.decode('utf-8'))
    print(csv_data)


# Example usage:
if __name__ == "__main__":
    bucket_name = 'harieminds'
    object_name = 'data.csv'

    csv_content = download_object(bucket_name, object_name)

    if csv_content is not None:
        # Now `csv_content` is a CSV file-like object, and you can use it with functions
        # or libraries that expect a file-like object, such as pandas.read_csv.

        # Example: Use pandas to read the CSV data from the file-like object
        import pandas as pd
        df = pd.read_csv(csv_content)

        # Now you have a pandas DataFrame (`df`) containing the data from the CSV file.
        # You can further process or analyze the data as needed.

        print(df)
