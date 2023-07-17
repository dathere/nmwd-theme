import json
import requests
from lxml import html

import ckan.plugins.toolkit as tk
import ckan.lib.captcha as captcha


def dataset_groups():
    '''Return a list of the groups in the dataset.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = tk.get_action('group_list')(
        data_dict={ 'all_fields': True})
    return groups


def topics_count():
    return len(dataset_groups())


def sources_count():
    orgs = tk.get_action('organization_list')(data_dict={})
    return len(orgs)


def datasets_count():
    datasets = tk.get_action('package_list')(data_dict={})
    return len(datasets)


def popular_datasets():
    package_list = tk.get_action('package_list')(data_dict={"limit": 500})
    pkg_dicts_list = []

    for package in package_list:
        package_dict = tk.get_action('package_show')(
                data_dict={'id': package, 'include_tracking': True})
        recent_views = package_dict["tracking_summary"]["recent"]
        package_dict["recent_views"] = recent_views
        pkg_dicts_list.append(package_dict)

    pkg_dicts_list.sort(key=lambda x: x["recent_views"], reverse=True)

    pkgs = pkg_dicts_list[:3]

    return pkgs


def get_tweets():
    url = "https://syndication.twitter.com/srv/timeline-profile/screen-name/NMWaterData"

    r = requests.get(url)

    # Using lxml html get script with id="__NEXT_DATA__" tag content
    tree = html.fromstring(r.content)
    tweets = json.loads(tree.xpath('//script[@id="__NEXT_DATA__"]').pop().text)["props"]

    five_latest_tweets = []

    for tweet in tweets["pageProps"]["timeline"]["entries"][:10]:
        five_latest_tweets.append(tweet["content"]["tweet"]["full_text"])

    return json.dumps(five_latest_tweets)


def is_valid_email(email):
    import re

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    objs = re.search(pattern, email)
    try:
        if objs.string == email:
            return True
    except:
        return False


def validate_contact_form(data_dict):
    errors = {}
    error_summary = {}

    for field, value in data_dict.items():
        if field in ('email', 'message') and not value.strip():
            errors[field] = ['Missing value']
            error_summary[field] = 'Missing value'

        elif field == 'email' and not is_valid_email(value):
            errors[field] = ['Invalid email address']
            error_summary[field] = 'Invalid email address'

        elif field == 'g-recaptcha-response':
            try:
                captcha.check_recaptcha(tk.request)
            except captcha.CaptchaError:
                errors['recaptcha'] = ['Bad Captcha. Please try again.']
                error_summary['recaptcha'] = 'Bad Captcha. Please try again.'

    return data_dict, errors, error_summary
