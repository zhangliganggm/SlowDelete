# -*- encoding:UTF-8 -*-
__author__ = 'Ace'
import os
import threading
import time


def get_speed_unit(value):
    if value > 1024 * 1024 * 1024:
        return str(value / 1024.0 * 1024 * 1024) + 'GB'

    elif value > 1024 * 1024:
        return str(value / (1024.0 * 1024)) + 'MB'

    elif value > 1024:
        return str(value / 1024.0) + 'KB'

    elif value > 0:
        return str(value) + 'B'


class SlowDelete(object):
    def __init__(self, filename, show_progress=True):
        """
        Input File or Folder
        :param filename: basestring
        """
        super(SlowDelete, self).__init__()

        self.filename = filename

        # KB MB/sec 5MB/s
        self.speed = 1024 * 1024 * 5

        self.total_size = 0
        self.delete_size = 0
        self.show_progress = show_progress

    def start(self):
        self.total_size = 0
        self.delete_size = 0

        self.counter_size()

        if os.path.isdir(self.filename):
            for root, dirs, files in os.walk(self.filename):
                for f in files:
                   self.delete_file(os.path.join(root, f))
        else:
            self.delete_file(self.filename)

        return True

    def set_speed(self, value):
        self.speed = value

    def hook(self, del_size):
        if not self.show_progress:
            return

        self.delete_size += del_size
        per = (self.delete_size / self.total_size) * 100
        print('{}%, Delete Speed:{}/s '.format(round(per), get_speed_unit(self.speed)))

    def counter_size(self):
        if not self.show_progress:
            return

        size = 0
        if os.path.isdir(self.filename):
            for root, dirs, files in os.walk(self.filename):
                for f in files:
                    size += os.path.getsize(os.path.join(root, f))
        else:
            size += os.path.getsize(self.filename)

        self.total_size = float(size)

    def delete_file(self, filename):
        file_size = os.path.getsize(filename)

        if file_size <= self.speed:
            os.remove(filename)
            self.hook(file_size)
            return True

        while True:
            file_size = os.path.getsize(filename)

            try:
                frw = open(filename, "r+b")
                frw.seek(file_size - self.speed, 0)

                frw.truncate()
                frw.close()

                self.hook(self.speed)

            except IOError, e:
                if e.errno == 22:
                    os.remove(filename)
                    self.hook(file_size)

            time.sleep(1)

        return True


class SlowDeleteThread(threading.Thread):
    
    def __init__(self, *args):
        super(SlowDeleteThread, self).__init__()
        self.work = SlowDelete(*args)

    def set_speed(self, value):
        self.work.set_speed(value)

    def run(self):
        self.work.start()

if __name__ == '__main__':
    # a = SlowDelete(u'tests\\big.file')
    # a.set_speed(1024*1024*5) # Delete Speed:5.0MB/s
    # a.start()
    # a.join()

    b = SlowDeleteThread(u'tests\\big.file')
    b.set_speed(1024*1024*0.1) # Speed:1024.0KB/s
    b.start()
    b.join()
