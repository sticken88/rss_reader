from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.models import SelectableDataItem
from kivy.uix.selectableview import SelectableView
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.factory import Factory

import feedparser
import webbrowser

# fetching data from rss url
url_to_read = "http://rss.cnn.com/rss/cnn_topstories.rss"
content = feedparser.parse(url_to_read)

# preparing the data structure: list of objects
title_list = {}

for item in content["items"]:
   title_list[item['title']] = {'title': item['title'], 'link': item['link'], 'is_selected': False}

Factory.register('SelectableView', cls=SelectableView)
Factory.register('ListItemButton', cls=ListItemButton)

# [TODO] Deselecting a selected item will terminate the application: fix it.
# [TODO] Improve the layout

#load the app layout
Builder.load_file('app_layout.kv')

# adapter class to handle the selected item
class FeedsDictAdapter(DictAdapter):

    # called every time that a new item is selected
    def rss_feed_changed(self, feeds_dict_adapter, *args):
       if len(feeds_dict_adapter.selection) == 0:
          return

       title = feeds_dict_adapter.selection[0].text
       url = title_list[title]['link']
       # open the url related to the selected item
       webbrowser.open(url)

# main class to handle the graphics rendering of the app
class MainView(GridLayout):

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(MainView, self).__init__(**kwargs)

        # the converter is used to create the list of object that can be selected
        list_item_args_converter = \
                lambda row_index, feed: {'text': feed['title'],
                                        'url': feed['link'],
                                        'is_selected': feed['is_selected'],
                                        'size_hint_y': None,
                                        'height': 30}

        # the actual list of items, created from the list of feeds and converted with the args_converter
        feeds_dict_adapter = \
                         FeedsDictAdapter(
                                   data=title_list,
                                   args_converter=list_item_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   template='CustomListItem')

        list_view = ListView(adapter=feeds_dict_adapter)

        self.add_widget(list_view)

        # bind the callback function executed every time a new item is selected
        feeds_dict_adapter.bind(on_selection_change = feeds_dict_adapter.rss_feed_changed)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=600))
