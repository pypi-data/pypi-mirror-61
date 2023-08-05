# Utluna Chart SVG Renderer

Using chrome-driver


## Installation

### !!! Important !!!
**Make sure you have chrome-driver installed**
On Alpine v3.10, run:
```bash
echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories
echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories
apk update
apk add chromium chromium-chromedriver

```

**Once chrome driver is successfully installed, install the library itself:**

Use the package manager pip to install ut2chartrenderer.
 
`pip` installation instructions are [here](https://pip.pypa.io/en/stable/installing/) 

```bash
pip install ut2chartrender
```




## Usage


Import library
```python
import ut2chartrender
```
Define settings in such way:
```python

settings = {
  "options": {
    "title": {
      "text": "Atmosphere Temperature by Altitude"
    },
    "subtitle": {
      "text": "According to the Standard Atmosphere Model"
    },
    "xAxis": {
      "reversed": false,
      "title": {
        "enabled": true,
        "text": "Altitude"
      },
      "labels": {
        "formatter": "function () { return this.value + \"km\"; }"
      },
      "maxPadding": 0.05,
      "showLastLabel": true
    },
    "yAxis": {
      "title": {
        "text": "Temperature"
      },
      "labels": {
        "formatter": "function () { return this.value + \"°\"; }"
      },
      "lineWidth": 2
    },
    "legend": {
      "enabled": true
    },
    "tooltip": {
      "headerFormat": "<b>{series.name}</b><br/>",
      "pointFormat": "{point.x} km: {point.y}°C"
    }
  },
  "datasets": [
    {
      "name": "Temperature by altitude",
      "series_type": "spline",
      "marker": {
        "enabled": true
      },
      "data": [
        [0, 15],[10, -50],[20, -56.5],[30, -46.5],[40, -22.1],[50, -2.5],[60, -27.7],[70, -55.7],[80, -76.5]
      ]
    }
  ]
}
```
Finally generate chart:
Way #1:
```python
svg_xml = ut2chartrender.generate_chart(**settings)

```
or way #2:

```python
svg_xml = ut2chartrender.generate_chart(
    options=settings["options"],
    datasets=settings["datasets"
)
```

If you dump `svg_xml` variable, you should see something like this:
```
<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg class="highcharts-root" height="400" style='font-family:"Lucida Grande", "Lucida Sans Unicode", Arial, Helvetica, sans-serif;font-size:12px;' version="1.1" viewbox="0 0 800 400" width="800" xmlns="http://www.w3.org/2000/svg">
```
which is an SVG file contents

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)