# pydexcom
Python API to interact with Dexcom Share API

```python
>>> dexcom = pydexcom.Dexcom('username', 'password')

>>> bg = dexcom.get_glucose_value()

>>> bg.value
105

>>> bg.trend_arrow
'→'

>>> bg.trend_description
'steady'
```
