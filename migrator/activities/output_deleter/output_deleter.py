import os
import shutil

from genrevive.core.base_activity import BaseActivity


class OutputDeleter(BaseActivity):
    PERMISSION_MODE = 0o755

    def __init__(self):
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]
        self.deleting_output = os.environ["DELETING_OUTPUT"]

    def execute(self):
        if self.deleting_output:
            for root, dirs, files in os.walk(self.angular_project_path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.chmod(file_path, mode=self.PERMISSION_MODE)
                        os.unlink(file_path)
                    except Exception as e:
                        print(f'Failed to delete file {file_path}. Reason: {e}')
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        os.chmod(dir_path, mode=self.PERMISSION_MODE)
                        shutil.rmtree(dir_path)
                    except Exception as e:
                        print(f'Failed to delete directory {dir_path}. Reason: {e}')
            try:
                shutil.rmtree(self.angular_project_path)
            except Exception as e:
                print(f'Failed to delete directory {self.angular_project_path}. Reason: {e}')
