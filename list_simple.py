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

url_to_read = "http://rss.cnn.com/rss/cnn_topstories.rss"

content = feedparser.parse(url_to_read)

title_list = {}
num = len(content["items"])
i=0
for item in content["items"]:
   title_list[i] = {'title': item['title'], 'link': item['link'], 'is_selected': False}
   i = i+1

# [TODO] Will SelectableView be in the kivy/factory_registers.py,
#        as a result of setup.py? ListItemButton? others?
Factory.register('SelectableView', cls=SelectableView)
Factory.register('ListItemButton', cls=ListItemButton)

# [TODO] SelectableView is subclassed here, yet, it is necessary to add the
#        index property in the template. Same TODO in list_cascade_images.py.

Builder.load_file('app_layout.kv')

class FeedsDictAdapter(DictAdapter):

    def rss_feed_changed(self, feeds_dict_adapter, *args):
       #print "Button pressed" + str(self.counter)
       feeds = feeds_dict_adapter.data

       webbrowser.open(feeds[0]['link'])
       print feeds[0]['link']
#       for feed in feeds:
#          print feed

       #print feeds_dict_adapter.data['text']
       #self.counter += 1
        #if len(fruit_categories_adapter.selection) == 0:
        #    self.data = {}
        #    return

        #category = \
        #        fruit_categories[fruit_categories_adapter.selection[0].text]
        #self.sorted_keys = category['fruits']

class MainView(GridLayout):
    '''Implementation of a list view with a kv template used for the list
    item class.
    '''

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(MainView, self).__init__(**kwargs)

        list_item_args_converter = \
                lambda row_index, feed: {'text': feed['title'],
                                        'url': feed['link'],
                                        'is_selected': feed['is_selected'],
                                        'size_hint_y': None,
                                        'height': 30}

        #feeds_sorted_titles = sorted(title_list.keys())

        feeds_dict_adapter = \
                         FeedsDictAdapter(
                                   #sorted_keys=[for i in range(num)],
                                   data=title_list,
                                   args_converter=list_item_args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   template='CustomListItem')

        list_view = ListView(adapter=feeds_dict_adapter)

        self.add_widget(list_view)

        # So far we created the converter, the adapter to populate the list view and then we added the list to the main view
        #detail_view = FruitDetailView(
        #        fruit_name=dict_adapter.selection[0].text,
        #        size_hint=(.7, 1.0))

        feeds_dict_adapter.bind(on_selection_change = feeds_dict_adapter.rss_feed_changed)


        #self.add_widget(detail_view)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=600))
