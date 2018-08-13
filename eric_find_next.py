import sublime
import sublime_plugin
import re

_special_chars_map = {i: '\\' + chr(i) for i in b'()[]?*+|^$\\.'}


class EricFindUnderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        # Check if the selection needs to be expanded to a word.
        for r in sel:
            if r.empty():
                self.view.window().run_command('find_under_expand')
                return
        # Take the last selection, and find the next one.
        last = sel[-1]
        expanded = sublime.Region(last.begin() - 1, last.end() + 1)
        text = self.view.substr(expanded)
        inner = text[1:-1]
        pattern = inner.translate(_special_chars_map)
        if not re.match(r'(\w\w)|(\W\W)', text[:2]):
            pattern = r'\b' + pattern
        if not re.match(r'(\w\w)|(\W\W)', text[-2:]):
            pattern = pattern + r'\b'
        #print('pattern=%r' % (pattern,))
        next = self.view.find(pattern, last.end())
        if next:
            sel.add(next)

# test_foo()
# test_bar
# test_foobar
# test_barfoo
# test_bar()
