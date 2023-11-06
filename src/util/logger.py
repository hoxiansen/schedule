import logging

init = False


def get_logger(debug=False) -> logging.Logger:
    log = logging.getLogger()
    global init
    if init:
        return log
    log_format = logging.Formatter(
        f'%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
    )

    # Console
    ch = logging.StreamHandler()
    log.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(log_format)
    log.addHandler(ch)

    # Log file
    # log_name = 'schedule.log'
    # fh = logging.FileHandler(log_name, mode='a', encoding='utf-8')
    # log.setLevel(logging.DEBUG if debug else logging.INFO)
    # fh.setFormatter(log_format)
    # log.addHandler(fh)
    init = True
    return log
