# GBIManager
A python extension for calculating global blockchain index

## Usage
### GBIManager.py
Create an object of GBIManager using file named base as the base file
```Python
gbiManager = GBIManager('base')
```
Calculate gbis using multiple sources
```Python
# using coinmarketcap as the only source
gbiManager.calculate_gbi(['coinmarketcap'])
# using other sources
gbiManager.calculate_gbi(['coinmarketcap', 'binance', 'kraken'])
```
Get calculated gbis
```Python
gbiManager.gbi
```
Example
```Python
gbiManager = GBIManager('base')
gbiManager.calculate_gbi(['coinmarketcap', 'binance', 'kraken'])
print(gbiManager.gbi)
```
Result
```Shell
{'coinmarketcap': (1515191961, 21267.434354247067), 'binance': (1515192129499, 20622.02891096077), 'kraken': (1515191961, 21124.81255298973)}
```
### Use Crontab to run extension schedulely

Type the following command to enter cronjob:

```Shell
$ crontab -e
```

To get crontab to insert data every 10 minutes

```shell
*/10 * * * * python [directory of main.py]
```

Save and close the file.
