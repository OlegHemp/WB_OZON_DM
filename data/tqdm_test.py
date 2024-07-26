from tqdm import tqdm
from tqdm import trange
from time import sleep


# # оборачиваем итератор range(100) классом tqdm()
# for i in tqdm(range(100), ncols=80, ascii=True, desc='Total'):
#     sleep(0.1)

# text = "\n"
# for char in tqdm(["a", "b", "c", "d"], ncols=80):
#     sleep(0.25)
#     text = text + char
#     tqdm.write(text)

# for i in trange(100, ncols=80, desc='Total'):
#     sleep(0.01)

import logging
from tqdm import trange
from tqdm.contrib.logging import logging_redirect_tqdm

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    with logging_redirect_tqdm():
        for i in trange(9):
            if i == 4:
                LOG.info("Ведение журнала консоли перенаправлено на `tqdm.write()`")
    # logging restored