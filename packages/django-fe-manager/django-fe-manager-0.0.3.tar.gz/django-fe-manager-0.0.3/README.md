# django-fe-manager

![PyPI](https://img.shields.io/pypi/v/django-fe-manager)
![Gitlab pipeline status](https://gitlab.com/antoniovazquezblanco/django-fe-manager/badges/master/pipeline.svg)
![Gitlab coverage](https://gitlab.com/antoniovazquezblanco/django-fe-manager/badges/master/coverage.svg)

Manage front end dependencies in Django


## Usage

Create a `FE_MANAGER` variable in your project settings defining the modules that can be used in your project. An example:
```python
FE_MANAGER = {
    'bootstrap': {
        'version': '4.0.0',
        'js': ['/static/js/bootstrap.bundle.min.js'],
        'css': ['/static/css/bootstrap.css', '/static/css/custom.css'],
        'dependencies': {'jquery'}
    },
    'jquery': {
        'version': '3.2.1',
        'js': ['/static/private/js/vendors/jquery-3.2.1.min.js']
    },
    'moment': {
        'version': '2.24.0',
        'js': ['https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment-with-locales.min.js']
    },
    'chartjs': {
        'version': '2.9.3',
        'js': ['https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js'],
        'dependencies': {'moment'}
    }
}
```

In your base view load the module, declare your dependencies, declare a dummy block at the beggining and add the css and js output tags:
```html
{% load fe_manager %}
{% fe_manager_add_module 'bootstrap' %}
{% fe_manager_add_module 'jquery' %}
{% block fe_manager %}{% endblock fe_manager %}
<!DOCTYPE html>
<html>
<head>
    <!-- Title and other HTML code... -->
    <!-- Output CSS -->
    {% fe_manager_output_css %}
</head>
<body>
    <!-- Content and other stuff... -->
    {% block content %}{% endblock content%}
    <!-- Output JS -->
    {% fe_manager_output_js %}
</body>
</html>
```

Every child view can now add its dependencies in the following way...
```html
{% extends 'base.html' %}

{% load fe_manager %}

{% block fe_manager %}
{% fe_manager_add_module 'chartjs' %}
{% endblock fe_manager %}

{% block content %}
Content here!
{% endblock content %}
```

The plugin will take care of dependency ordering and outputting both JS and CSS to your base template!
