
# Weather Dash

Visualize weather data with highly customizable interative dashboard, plotly DASH.

<img width="1491" alt="image" src="https://github.com/Pamekitti/weather-dash/assets/93110244/9452678b-f926-4bd3-8ec5-93e3759f6908">

## Link 
http://weatherdash.gdbqbeapbmehasbr.southeastasia.azurecontainer.io/


## Installation

Install my-project with npm

```bash
  pip install -r requirements.txt
```

To run DASH on your local computer, in file index.py, change

```python
app_port = os.environ['APP_PORT']
```

To

```python
app_port = '80
```


## Deployment

To deploy this project run

```bash
  docker build --tag name .
```

On mac Apple Silicon
```bash
docker buildx build --platform=linux/amd64 -t name .
```

Then
```bash
  docker push name
```
Deploy using Azure Container Instance Services

