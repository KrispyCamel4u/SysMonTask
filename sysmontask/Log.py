import logging

logging.basicConfig(filename="/tmp/sysmontask.log",
                    filemode="w",
                    format="%(filename)s : %(levelname)s : %(funcName)s : %(message)s"
                    )

class Log:
    """Static class for keeping the level variable same throughput the files."""
    LEVEL=40
    @staticmethod
    def getLogger(name="root"):
        logger= logging.getLogger(name)
        logger.setLevel(Log.LEVEL)
        return logger

class staticVar:
    logger= None
    current_column=None
    saved_column=None
    cgroups_enabled=None