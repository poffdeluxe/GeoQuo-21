# GeoQuo-21

A cleaner re-write of my local timezone API [GeoQuo](https://github.com/poffdeluxe/GeoQuo) written in python and integrated with 21.co
I was going to try and integrate with the 21.co marketplace but Heroku doesn't seem to be supported right now :(

Currently live on Heroku at: `https://geoquo21.herokuapp.com`

Example usage: `21 buy "https://geoquo21.herokuapp.com/Beijing"`

## Sample Routes

#### Pull time information for a specified city
```
/Beijing
```


#### Pull time information for a specified city with country code
```
/time/Beijing/CN
```


#### Pull time information for a specified city in the US
```
/time/Buffalo/US/MN
```
