from kivy.adapters.dictadapter import DictAdapter
from kivy.adapters.models import SelectableDataItem
from kivy.uix.selectableview import SelectableView
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.factory import Factory

import feedparser

url_to_read = "http://rss.cnn.com/rss/cnn_topstories.rss"

content = feedparser.parse(url_to_read)

title_list = {}
num = len(content["items"])
i=0
for item in content["items"]:
   title_list[str(i)] = {'text': item['title'], 'is_selected': False}
   i = i+1

#integers_dict = { str(i): {'text': str(i), 'is_selected': False} for i in range(100)}

# [TODO] Will SelectableView be in the kivy/factory_registers.py,
#        as a result of setup.py? ListItemButton? others?
Factory.register('SelectableView', cls=SelectableView)
Factory.register('ListItemButton', cls=ListItemButton)

# [TODO] SelectableView is subclassed here, yet, it is necessary to add the
#        index property in the template. Same TODO in list_cascade_images.py.

Builder.load_string('''
[CustomListItem@SelectableView+BoxLayout]:
    size_hint_y: ctx.size_hint_y
    height: ctx.height
    ListItemButton:
        text: ctx.text
        is_selected: ctx.is_selected
''')


class MainView(GridLayout):
    '''Implementation of a list view with a kv template used for the list
    item class.
    '''

    def __init__(self, **kwargs):
        kwargs['cols'] = 1
        super(MainView, self).__init__(**kwargs)

        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['text'],
                                        'is_selected': rec['is_selected'],
                                        'size_hint_y': None,
                                        'height': 30}

        # Here we create a dict adapter with 1..100 integer strings as
        # sorted_keys, and integers_dict from fixtures as data, passing our
        # CompositeListItem kv template for the list item view. Then we
        # create a list view using this adapter. args_converter above converts
        # dict attributes to ctx attributes.
        dict_adapter = DictAdapter(sorted_keys=[str(i) for i in range(num)],
                                   data=title_list,
                                   args_converter=list_item_args_converter,
                                   template='CustomListItem')

        list_view = ListView(adapter=dict_adapter)

        self.add_widget(list_view)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=600))