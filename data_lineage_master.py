import yaml


class DataLineageMaster:
    """
    Core instance of program
    """

    def tst(self):
        pass


if __name__ == '__main__':
    with open("config.yml", "r") as yml_file:
        cfg = yaml.load(yml_file)
