import matplotlib.pyplot as plt
import pandas as pd

data = {
    'Time': pd.date_range(start='2024-03-16', periods=31, freq='D'),
    'Delivered': [34, 27, 25, 24, 29, 24, 25, 25, 24, 19, 15, 19, 12, 17, 16, 17, 14, 16, 16, 11, 13, 14, 10, 7, 8, 7, 4, 4, 4, 4, 5],
    'Received': [46, 27, 26, 24, 29, 24, 26, 26, 25, 19, 15, 19, 12, 17, 16, 17, 14, 16, 16, 11, 13, 15, 10, 7, 8, 7, 4, 4, 4, 4, 5],
    'Response Rate': [73.9, 100, 96.2, 100, 100, 100, 96.2, 96.2, 96, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 93.3, 100, 100, 100, 100, 100, 100, 100, 100, 100]
}
df = pd.DataFrame(data)

plt.figure(figsize=(15, 7))
plt.plot(df['Time'], df['Delivered'], label='Delivered Emails', marker='o', color='blue')
plt.plot(df['Time'], df['Received'], label='Received Emails', marker='^', color='red')
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(df['Time'], df['Response Rate'], label='Response Rate', color='green', linestyle='--', marker='s')

start_date = pd.to_datetime('2024-03-16')
end_date = df['Time'].iloc[-1]
date_range = pd.date_range(start=start_date, end=end_date, freq='3D')

ax.set_xticks(date_range)
ax.set_xticklabels([dt.strftime('%m-%d') for dt in date_range])

ax.legend(loc='upper left', bbox_to_anchor=(0.1, 1.15))
ax2.legend(loc='upper right', bbox_to_anchor=(0.9, 1.15))

plt.title('Daily Email Delivery and Response Rates')
plt.xlabel('Date')
ax.set_ylabel('Email Count')
ax2.set_ylabel('Response Rate (%)')

plt.grid(True)

plt.tight_layout()
plt.show()
