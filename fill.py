from random import randint
import subprocess
from datetime import datetime, timedelta

st = list(map(int, input('initial date (YYYY-MM-DD):\n').split('-')))
fn = list(map(int, input('end date (YYYY-MM-DD):\n').split('-')))

start = datetime(*st).date()
end = datetime(*fn).date()
days = (end-start).days
dates = [start + timedelta(days=idx) for idx in range(days)]

def gcommit(date: datetime.date) -> None:
    with open('dots.txt', 'a') as f:
        f.write('.\n')
    subprocess.call(['git', 'commit', '-am', "'add commit'", '--date', f'{date}'])

for date in dates:
    for coms in range(randint(1, 5)):
        gcommit(date)

subprocess.call(['git', 'pull', 'origin', 'main'])
