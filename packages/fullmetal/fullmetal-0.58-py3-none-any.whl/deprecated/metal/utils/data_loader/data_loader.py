import boto3
from botocore.exceptions import NoCredentialsError
import sys
from google_images_download import google_images_download
import os
import shutil
from deprecated.metal.utils.production_util import create_training_data as create_training_data_
from dotenv import load_dotenv
import os
from os.path import join, dirname

response = google_images_download.googleimagesdownload()

class Data_loader(object):
    """docstring for data_loader."""

    def __init__(self, path=None):
        super(Data_loader, self).__init__()
        self.output_directory = path

    def init_s3(self, env_path=None):

        load_dotenv(env_path)
        AWSAccessKeyId = os.getenv("AWSAccessKeyId")
        AWSSecretKey = os.getenv("AWSSecretKey")
        region = os.getenv("region")

        self.s3 = boto3.client('s3', aws_access_key_id=AWSAccessKeyId,
                          aws_secret_access_key=AWSSecretKey)

    def upload_to_awsS3(self, local_file, bucket, s3_file):
        try:
            self.s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def download(self, query, image_directory, format="jpg",print_urls=True, limit=100, size="medium", aspect_ratio="panoramic",type_="photo", output_directory=None):
        #bug: should check if downloads dir alrady exist
        #need to be instacnce var
        if output_directory == None:
            self.output_directory

        arguments = {"keywords": query,
             "format": format,
             "limit":limit,
             "print_urls":print_urls,
             "size": size,
             "aspect_ratio": aspect_ratio,
             "type":type_,
             "output_directory":self.output_directory,
             "image_directory":image_directory}
        try:
            response.download(arguments)
        # Handling File NotFound Error
        except FileNotFoundError:
            arguments = {"keywords": query,
                 "format": format,
                 "limit":limit,
                 "print_urls":print_urls,
                 "size": size,
                 "aspect_ratio": aspect_ratio,
                 "type":type_,
                 "output_directory":self.output_directory,
                 "image_directory":image_directory}
            # Providing arguments for the searched query
            try:
                # Downloading the photos based
                # on the given arguments
                response.download(arguments)
            except:
                pass

    def create_training_data(self,classes,img_size=50):
        return create_training_data_(img_size=img_size, classes=classes, data_dir=self.output_directory, color=None)

    def delete_dir(self):
         shutil.rmtree(self.output_directory)
