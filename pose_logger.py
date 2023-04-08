import os
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler
log_file = 'app.log'
# if os.path.exists(log_file):
#     # if log file exists, delete it before recreating it
#     print('\n\nDeleting log file: ', log_file)
#     print('Creating new log file: ', log_file, '\n\n')
#     os.remove(log_file)
#     f = open(log_file, 'w')
#     f.close()
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)