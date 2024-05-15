import subprocess
import os
import datetime
import logging

log_file = "/var/log/backup"

def upload_files_to_drive(source_path, destination_path, file):
    with open(log_file, 'a') as log:
        try:
            # Verify if destination exists in remote
            if check_remote_file(destination_path):
                log.write("File already exists on the remote. Skipping upload.\n")
                return

            # Upload files to drive
            command = f"rclone copy {source_path} {destination_path.rstrip(file)}"
            subprocess.run(command, shell=True, check=True)
            log.write("{} --- Upload successful.\n".format(datetime.datetime.now()))
        except subprocess.CalledProcessError as e:
            log.write("{} --- Error uploading: {}\n".format(datetime.datetime.now(),e.output))

def check_remote_file(remote_path):
    try:
        command = f"rclone ls {remote_path}"
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return True  # File exists
    except subprocess.CalledProcessError as e:
        logger= logging.getLogger()
        logger.error('Failed process rclone %s', e)
        return False  # File does not exist

def calculate_checksum(file_path):
    try:
        command = f"rclone hashsum sha256 {file_path}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        with open(log_file, 'a') as log:
            log.write("Error calculating checksum: {}\n".format(e.output))
        return None

def main():
    source_directory = "/mnt/volume-nyc1-01/web/media/"
    remote_drive = "drive:/mnt/volume-nyc1-01/web/media/"

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, source_directory)
            remote_file_path = os.path.join(remote_drive, relative_path)
            with open(log_file, 'a') as log:
                log.write("{} --- Processing: {}\n".format(datetime.datetime.now(),file_path))

                # Upload files to drive
                upload_files_to_drive(file_path, remote_file_path, file)

                # Verify checksum
                uploaded_checksum = calculate_checksum(remote_file_path)
                local_checksum = calculate_checksum(file_path)

                if uploaded_checksum == local_checksum:
                    log.write("Checksum verified. File uploaded successfully.\n")
                else:
                    log.write("Checksum mismatch. File upload failed.\n")

if __name__ == "__main__":
    main()
