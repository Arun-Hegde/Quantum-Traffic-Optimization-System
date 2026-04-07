import logging, os

def setup_logger(name: str = "app") -> logging.Logger:
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        fh = logging.FileHandler("logs/app.log", encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(ch)
        logger.addHandler(fh)
    return logger
