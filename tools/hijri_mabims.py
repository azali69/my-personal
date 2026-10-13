"""Hijri month starts for Singapore by the MABIMS 2021 criteria that MUIS uses (moon at least 3 deg above the horizon and
at least 6.4 deg from the sun at sunset after the conjunction; otherwise the month has 30 days). Positions by PyEphem.
Checked against Singapore's 1 Ramadan / Hari Raya Puasa / Hari Raya Haji dates 2023-2026: all match.
Output: prayer/hijri.json {"start":[y,m] of the first month, "days":[ISO date of the 1st of each month, ...]}"""
import ephem, datetime, math, json, os
SG=ephem.Observer(); SG.lat='1.3521'; SG.lon='103.8198'; SG.elevation=0; SG.pressure=0; SG.horizon='-0:50'
def ok(day):
    SG.date=ephem.Date(datetime.datetime(day.year,day.month,day.day,4,0)); ss=SG.next_setting(ephem.Sun()); SG.date=ss
    m=ephem.Moon(SG); s=ephem.Sun(SG)
    return ephem.previous_new_moon(ss)<ss and math.degrees(m.alt)>=3 and math.degrees(ephem.separation(m,s))>=6.4
starts=[]; nm=ephem.next_new_moon('2018-09-05')
while ephem.Date(nm).datetime().year<2049:
    d=ephem.Date(nm+8*ephem.hour).datetime().date()
    for k in range(3):
        if ok(d+datetime.timedelta(days=k)): starts.append((d+datetime.timedelta(days=k+1)).isoformat()); break
    nm=ephem.next_new_moon(nm+1)
assert starts[0]=='2018-09-11', starts[0]   # 1 Muharram 1440 in Singapore
os.makedirs('prayer',exist_ok=True)
json.dump({'source':'Calculated with the MABIMS 2021 criteria (altitude 3 deg, elongation 6.4 deg) for Singapore, as MUIS uses','start':[1440,1],'days':starts},open('prayer/hijri.json','w'),separators=(',',':'))
print(len(starts), starts[:3], starts[-1])
