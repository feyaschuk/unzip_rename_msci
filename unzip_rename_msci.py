import os
from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential
import zipfile
import argparse
import io

token_credential = ClientSecretCredential("tenant-id", "client-id", "client-secret")

OAUTH_STORAGE_ACCOUNT_NAME = "prodeastus2data"
oauth_url = f"https://{OAUTH_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"

blob_service_client = BlobServiceClient(account_url=oauth_url, credential=token_credential)

count = 0
count_if_exist = 0


def get_blob_list():
    '''Extracts list of files named with a specific prefix and date.'''

    dr_dir = blob_service_client.get_container_client(namespace.container_name)
    blob_list = [x for x in dr_dir.list_blobs(name_starts_with="raw/" + namespace.prefix)
                 if namespace.filter_date in (x.name).split('_').pop()]
    if not blob_list:
        print(f"There are no files which starts with raw/{namespace.prefix}.")
    return blob_list


def unpack_rename_files(blob_list, count, count_if_exist):
    '''Extracts csv file to clipboard, renames if needed and saves it in dropdir/msci/esg/ folder.'''

    dr_dir = blob_service_client.get_container_client(namespace.container_name)
    for blob in blob_list:
        blob_name = blob.name
        print(f"{blob_name} file found and unpacking process started.")
        blob = blob_service_client.get_blob_client(namespace.container_name, blob_name)
        with io.BytesIO() as b:
            download_stream = blob.download_blob(0)
            download_stream.readinto(b)
            with zipfile.ZipFile(b, compression=zipfile.ZIP_LZMA) as z:
                for filename in z.namelist():
                    basename = os.path.splitext(filename)[0]
                    feed = basename.removeprefix(namespace.prefix).removesuffix(namespace.filter_date)[:-1]
                    if not filename.endswith('/'):
                        with z.open(filename, mode='r', pwd=b'') as f:
                            if len(feed) == 0:
                                filename = "SECURITIES_ALL_SECURITIES_ALL_20221104.txt"
                            elif len(feed) > 50:
                                filename = "SECURITIES_ALL_COMP_SOCIAL_AND_CORPORATE_BEHAVIOR_QUAL_INDICATORS_20221104.txt"
                            else:
                                filename = filename

                            if dr_dir.get_blob_client("dropdir/msci/esg/" + filename).exists():
                                count_if_exist += 1
                                print(f"{filename} already exists")
                            else:
                                dr_dir.get_blob_client("dropdir/msci/esg/" + filename).upload_blob(f)
                                count += 1
                print(f"{count} file(s) uploaded successfully. "
                      f"{count_if_exist} file(s) already existed in {namespace.container_name}/dropdir/msci/esg.")


def create_parser():
    ''' Reads and adds argument values from the command line.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('filter_date')
    parser.add_argument('prefix')
    parser.add_argument('container_name')
    return parser


if __name__ == "__main__":

    parser = create_parser()
    namespace = parser.parse_args()
    blob_list = get_blob_list()
    unpack_rename_files(blob_list, count, count_if_exist)
