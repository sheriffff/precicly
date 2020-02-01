# precicly

Live prediction of bicycle waiting times for Madrid and Barcelona.

## Reproducing results

### Package mangement

After cloning the repository:

1. Make sure you have conda installed. 
2. Create a new conda environment: run `conda env create --file=requirements.yml` from the root of the repository. 
This should create an environment called `precicly` with the same libraries' versions. 

In case a new package is needed:
1. Install the package locally.
2. Rewrite `requirements.yml` with `conda env export > requirements.yml`
3. Other contributors will have to run `conda env create --file=requirements.yml` to update their own environments.

(This is for the moment a bit cumbersome, but let's improve it)


### Madrid API calls

#### BiciMad

To be able to mimic our API calls, you will need to:
1. Log in as a developer in https://mobilitylabs.emtmadrid.es/
2. Create a new application, which will provide you with some credentials.
3. Create a file `auth_credentials.py` in `precicly/madrid/` with the following:

``` auth_bicimad = {
        'email': string with your email,
        'password': string with your password,
        'X-ClientId': string with X-ClientId,
        'X-ApiKey': string with X-ApiKey,
        'passKey': string with passKey
}
```

#### Weather Madrid

Currently not implemented

### Barcelona API Calls

#### Bicing Barcelona

The Bicing API doesn't require an API key

#### Weather Barcelona

To reproduce the results from Barcelona you'll need to get an API for the [Open Weather Map API](https://openweathermap.org/). Register at their website, grab the API key and save it in `./barcelona/weather_barcelona_token.txt` as 

```
your API key should only be one line
```

Everything else should be read by the programme.
