# import re
# import os
#
# from secret import MAIL_ARCHIVE_DIR
#
#
# emails_dir_path = MAIL_ARCHIVE_DIR
#
# timestamp_regex = re.compile(r"TIME:\s*(\d+)")
#
# timestamps = []
#
# for filename in os.listdir(emails_dir_path):
#     if filename.endswith('.txt'):
#         file_path = os.path.join(emails_dir_path, filename)
#         with open(file_path, 'r') as file:
#             file_content = file.read()
#             match = timestamp_regex.search(file_content)
#             if match:
#                 timestamps.append(int(match.group(1)))
#
# print(timestamps)

from datetime import datetime, timedelta
import pytz

gmt_zone = pytz.timezone('GMT')
bst_zone = pytz.timezone('Europe/London')

# gmt and utc are the same in winter
now_utc = datetime.utcnow()
now_gmt = gmt_zone.localize(now_utc)

is_dst_now = now_gmt.astimezone(bst_zone).dst() != timedelta(0)

# 打印当前是否为夏令时
print("Is it currently BST (Daylight Saving Time)?", is_dst_now)

# check if now is bst_zone(3.31-10.27)
if is_dst_now:
    # transform gmt to bst
    now_bst = now_gmt.astimezone(bst_zone)
    today_bst = now_bst.replace(hour=0, minute=0, second=0, microsecond=0)
    day_before_today_bst = today_bst - timedelta(days=1)
    # RFC 2822 format with the BST offset
    one_day_ago = day_before_today_bst.strftime('%a, %d %b %Y %H:%M:%S %z')
else:
    today_gmt = now_gmt.replace(hour=0, minute=0, second=0, microsecond=0)
    day_before_today_gmt = today_gmt - timedelta(days=1)
    # RFC 2822 format with the GMT offset
    one_day_ago = day_before_today_gmt.strftime('%a, %d %b %Y %H:%M:%S %z')

print("RFC 2822 formatted timestamp for the start of yesterday:", one_day_ago)


