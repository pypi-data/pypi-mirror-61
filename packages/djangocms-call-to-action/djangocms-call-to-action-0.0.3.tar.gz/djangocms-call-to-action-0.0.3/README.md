djangocms-call-to-action
==========================

A djangocms plugin that allows you to create Call To Action (CTA) indicators, to display them as buttons in a Django CMS plugin, to track user click on these buttons on a GA conversion tunnel. Each CTA is linked with a fobi form which registers the user email in a given mailing list.

This project is a WIP and might need some improvements.

## Installation

This plugin requires `Django-CMS`, `sendgrid`, `django-fobi`.


 1. Install module using pipenv:
 ```
 pipenv install djangocms-call-to-action
 ```
 * *Or pip:*
 ```
 pip install djangocms-call-to-action
 ```
 2. Add it to your installed apps:
 ```
     "djangocms_call_to_action",
 ```
 3. Apply migrations
 ```
 py manage.py migrate djangocms_call_to_action
 ```
 4. Include your sendgrid api key in your settings
 ```python
 DJANGOCMS_CTA_SENDGRID_API_KEY = "YOUR_API_KEY"
 ```
 * *Or load it using an environment var:*
 ```python
 import os
 DJANGOCMS_CTA_SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", None)
 ```
 5. Include your Google analytics GA code in your settings
 ```python
 DJANGOCMS_CTA_GA_UA = "UA-*******-*"
 ```
 * *Or load it using an environment var:*
 ```python
 import os
 DJANGOCMS_CTA_GA_UA = os.getenv("GA_UA", None)
 ```

 6. Include the CTAFobiFormWidgetRedirectMiddleware before all other middlewares, and CTAPagePermissionMiddleware after django-cms CurrentPageMiddleware:

 ```python
  MIDDLEWARE = (
    "djangocms_call_to_action.middleware.CTAFobiFormWidgetRedirectMiddleware",
    ...
    "cms.middleware.page.CurrentPageMiddleware",
    ...
    "djangocms_call_to_action.middleware.CTAPagePermissionMiddleware",
)
 ```

 7. Add `djangocms_call_to_action.urls` to your urls:

 ```python
  urlpatterns = [
    ...
    path("cta/", include("djangocms_call_to_action.urls")),
    ...
    re_path("^", include("cms.urls")),
]

 ```

## Optional settings

 1. Configure templates used to display the CMS plugin
 ```python
 from django.utils.translation import ugettext_lazy as _

 DJANGOCMS_CTA_TEMPLATES = (("default.html", _("Link")), ("button_primary.html", _("Button primary")), ("button_secondary.html", _("Button secondary")),)
 ```

 2. Activate select2 for cms page selectors (requires django-select2)
 ```python
 DJANGOCMS_CTA_USE_SELECT2 = True
 ```

 3. Configure labels used for actions in GA
 ```python
 DJANGOCMS_CTA_DISPLAYED_USER_GA_LABEL = "Affiché"
 DJANGOCMS_CTA_CLICKED_USER_GA_LABEL = "Cliqué"
 DJANGOCMS_CTA_CONVERTED_USER_GA_LABEL = "Converti"
 ```

 4. Change cache duration for deny pages ids
 ```python
 DJANGOCMS_CTA_DENY_PAGES_IDS_CACHE_DURATION = 24 * 60 * 60 # Cache for 24h
 ```

## How to use

 1. Create a fobi form using fobi interface.

 In order to work properly with sendgrid registration, the form must contains the following fields:
    - First name
    - Last name
    - Email
    - An opt-in checkbox to consent the user email registration on sendgrid list

 2. Add the sendgrid handler to register the email address of the user into

 3. Create a CMS page to display the fobi form into

 4. Insert the fobi form into the new page, using the CMS plugin "Call to Action"

 5. On the django admin, create a Campaign linked with the CMS page created on step 4.
 Choose where the user will be redirected on form validation:
    - To an external link
    - To an internal link
    - To a file

 You can choose to deny the access to the page if the form was not validated by the user.

 6. On your content, insert some CTA plugins to redirect to the form using the "Click To Action" cms plugin


