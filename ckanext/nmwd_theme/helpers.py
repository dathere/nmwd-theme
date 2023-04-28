from pylons import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model.tracking import TrackingSummary
import requests
from lxml import html
import json

# use the env function
import ckan.lib.helpers as h

from datetime import datetime

def dataset_groups():
    '''Return a list of the groups in the dataset.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={ 'all_fields': True})
    return groups


def topics_count():
    return len(dataset_groups())

def sources_count():
    orgs = toolkit.get_action('organization_list')(data_dict={})
    return len(orgs)

def datasets_count():
    datasets = toolkit.get_action('package_list')(data_dict={})
    return len(datasets)

def popular_datasets():
    package_list = toolkit.get_action('package_list')(data_dict={"limit": 500})
    pkg_dicts_list = []

    for package in package_list:
        package_dict = toolkit.get_action('package_show')(
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

    return five_latest_tweets
    