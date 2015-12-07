import time
import sys, getopt
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import subprocess


class CustomPatternMatchingEventHandler(PatternMatchingEventHandler):
    def __init__(self, folder_to_listen, bucket_path, patterns=None):
        super(self.__class__, self).__init__(patterns=patterns)
        self.folder_to_listen = folder_to_listen
        self.bucket_path = bucket_path

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        p = subprocess.Popen(
            ['aws', 's3', 'cp', file_path, bucket_path, '--recursive'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out

    def on_deleted(self, event):
        self.process(event)


if __name__ == '__main__':

    try:
        args = sys.argv[1:]
        opts, args = getopt.getopt(args, 'hf:b:p:', ['folder=', 'bucket_path=', 'file_patterns='])

        for opt, arg in opts:
            if opt == '-h':
                print('file.py -f <folder_to_listen> -b <bucket_path> -p <file_patterns sep. comma>')
                sys.exit()
            elif opt in ("-f", "--folder"):
                file_path = arg
            elif opt in ("-b", "--bucket_path"):
                bucket_path = arg
            elif opt in ("-p", "--file_patterns"):
                patterns = arg.strip().split(',')

        observer = Observer()
        observer.schedule(CustomPatternMatchingEventHandler(patterns), path=file_path)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    except getopt.GetoptError as exc:
        print exc
        print('file.py -f <folder_to_listen> -b <bucket_path> -e <file_extensions sep. comma>')
        sys.exit(2)
    except BaseException as exc:
        print(exc)
        sys.exit(3)
