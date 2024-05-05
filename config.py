from PyQt5.QtCore import QObject, pyqtSignal
import configparser

class Config(QObject):
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()

    def read_config(self):
        try:
            self.config.read("config.ini", encoding="utf-8")
            return self.config
        except configparser.Error as e:
            self.error_occurred.emit("Error reading config: {}".format(str(e)))
            return None

    def write_config(self, settings):
        try:
            for section, options in settings.items():
                self.config[section] = options

            with open("config.ini", "w") as config_file:
                self.config.write(config_file)
        except configparser.Error as e:
            self.error_occurred.emit("Error writing config: {}".format(str(e)))