import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

import ckanext.nmwd_theme.helpers as helpers
import ckanext.nmwd_theme.views as views


class Nmwd_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer, inherit=True) 
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, 'templates')
        tk.add_public_directory(config_, 'public')
        tk.add_resource('assets', 'nmwd_theme')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'nwmd_theme_dataset_groups': helpers.dataset_groups,
            'nmwd_theme_popular_datasets': helpers.popular_datasets,
            'nmwd_theme_topics_count': helpers.topics_count,
            'nmwd_theme_sources_count': helpers.sources_count,
            'nmwd_theme_datasets_count': helpers.datasets_count,
            'nmwd_theme_get_tweets': helpers.get_tweets,
            'nwmd_theme_showcases': helpers.showcases,
            'get_value_from_showcase_extras': helpers.get_value_from_showcase_extras,
        }

    # IBlueprint
    def get_blueprint(self):
        return views.get_blueprints()
