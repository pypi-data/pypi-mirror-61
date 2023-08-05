flask-satella-metrics
=====================
[![Build Status](https://travis-ci.org/piotrmaslanka/flask-flask-satella-metrics-metrics.svg)](https://travis-ci.org/piotrmaslanka/flask-flask-satella-metrics-metrics)
[![Test Coverage](https://api.codeclimate.com/v1/badges/34b392b61482d98ad3f0/test_coverage)](https://codeclimate.com/github/piotrmaslanka/flask-flask-satella-metrics-metrics/test_coverage)
[![Code Climate](https://codeclimate.com/github/piotrmaslanka/flask-flask-satella-metrics-metrics/badges/gpa.svg)](https://codeclimate.com/github/piotrmaslanka/flask-flask-satella-metrics-metrics)
[![Issue Count](https://codeclimate.com/github/piotrmaslanka/flask-flask-satella-metrics-metrics/badges/issue_count.svg)](https://codeclimate.com/github/piotrmaslanka/flask-flask-satella-metrics-metrics)
[![PyPI](https://img.shields.io/pypi/pyversions/flask-flask-satella-metrics-metrics.svg)](https://pypi.python.org/pypi/flask-flask-satella-metrics-metrics)
[![PyPI version](https://badge.fury.io/py/flask-flask-satella-metrics-metrics.svg)](https://badge.fury.io/py/flask-flask-satella-metrics-metrics)
[![PyPI](https://img.shields.io/pypi/implementation/flask-flask-satella-metrics-metrics.svg)](https://pypi.python.org/pypi/flask-flask-satella-metrics-metrics)

flask-satella-metrics is an application to seamlessly measure your Flask application using Satella's metrics.

Example use:

```python
from flask_satella_metrics import SatellaMetricsMiddleware
app = flask.Flask(__name__)
SatellaMetricsMiddleware(app)
```

And to launch a Prometheus exporter use the following snippet:

```python
from satella.instrumentation.metrics.exporters import PrometheusHTTPExporterThread
phet = PrometheusHTTPExporterThread('0.0.0.0', 8080, {'service_name': 'my_service'})
phet.start()
```
