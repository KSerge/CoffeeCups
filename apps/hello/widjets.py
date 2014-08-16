from django.forms import TextInput


class CalendarWidget(TextInput):
    class Media:
        css = {
            'all': ('http://code.jquery.com/ui/1.11.0/themes/smoothness/jquery-ui.css',)
        }
        js = ('js/datepicker.js',)