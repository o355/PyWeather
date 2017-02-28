## Updater for PyWeather

PyWeather uses a .json file, in which build numbers are compared.

Build numbers are creatively sequenced by removing the dots.

0.3 beta's build number is 30. 0.3.1 beta's BN is 31. 0.4 beta = 40. 1.0 = 100, and so on.

The updater's API version shows the API version of said updater. If the updater API moves on to v2, I'll keep the legacy v1 API as well.
