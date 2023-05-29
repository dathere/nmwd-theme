import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from helpers import *


class Nmwd_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer) 
    plugins.implements(plugins.IRoutes, inherit=True)
    # IConfigurer


    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nmwd_theme')

        # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers)
    def get_helpers(self):
        '''Register the dataset_groups function above as a template
        helper function.

        '''
        return {
            'nwmd_theme_dataset_groups': dataset_groups, \
            'nmwd_theme_popular_datasets': popular_datasets, \
            'nmwd_theme_topics_count': topics_count, \
            'nmwd_theme_sources_count': sources_count, \
            'nmwd_theme_datasets_count': datasets_count, \
            'nmwd_theme_get_tweets': get_tweets
            }


    # def before_map(self, m):
    #     m.connect('ckanext_showcase_test', '/test', action='test')
    def before_map(self, m):
        m.connect('team', #name of path route
            '/team', #url to map path to
            controller='ckanext.nmwd_theme.controller:NMWDController', #controller
            action='team') #controller action (method)
        m.connect('map', 
            '/map', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='map')             
        m.connect('news', 
            '/news', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='news') 
        m.connect('faq', 
            '/faq', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='faq') 
        m.connect('contact', 
            '/contact', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='contact') 
        m.connect('reports', 
            '/reports', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='reports') 
        m.connect('photos', 
            '/photos', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='photos') 
        m.connect('events', 
            '/events', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='events')       
        m.connect('contactmail', 
            '/contactmail', 
            controller='ckanext.nmwd_theme.controller:NMWDController', 
            action='contactmail')                          
        return m