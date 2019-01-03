import sublime
import sublime_plugin


class EricDupeTestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.window().show_input_panel(
            'Enter Count', '400', self.on_done, None, None)

    def on_done(self, text):
        self.view.run_command('eric_dupe_test_complete', {'count': text})


class EricDupeTestCompleteCommand(sublime_plugin.TextCommand):

    def run(self, edit, count=''):
        fn_name = sublime.get_clipboard()
        txt = ['#[test] fn %s%i() { %s(); }' % (fn_name, i, fn_name) for i in range(0, int(count))]
        self.view.insert(edit, self.view.sel()[0].begin(), '\n'.join(txt))


# def print_id_vel(where, view):
#     pass
#     print('VEL %s: view.id=%s buffer_id=%s %s' % (where, view.id(), view.buffer_id(), view.file_name()))


# class EricListener2(sublime_plugin.ViewEventListener):

#     # @classmethod
#     # def is_applicable(cls, settings):
#     #     s = settings.get('syntax')
#     #     return s == 'Packages/Rust Enhanced/RustEnhanced.sublime-syntax'
#         # return
#         # return util.is_rust_view(settings)

#     @classmethod
#     def applies_to_primary_view_only(cls):
#         return False

#     def on_new(self):
#         print_id_vel('on_new', self.view)

#     def on_new_async(self):
#         print_id_vel('on_new_async', self.view)

#     def on_clone(self):
#         print_id_vel('XXXX on_clone', self.view)

#     def on_clone_async(self):
#         print_id_vel('XXXX on_clone_async', self.view)

#     def on_load(self):
#         print_id_vel('on_load', self.view)

#     def on_load_async(self):
#         print_id_vel('on_load_async', self.view)

#     def on_pre_close(self):
#         print_id_vel('on_pre_close', self.view)

#     def on_close(self):
#         print_id_vel('on_close', self.view)

#     def on_pre_save(self):
#         print_id_vel('on_pre_save', self.view)

#     def on_pre_save_async(self):
#         print_id_vel('on_pre_save_async', self.view)

#     def on_post_save(self):
#         print_id_vel('on_post_save', self.view)

#     def on_post_save_async(self):
#         print_id_vel('on_post_save_async', self.view)

#     def on_modified(self):
#         print_id_vel('on_modified', self.view)

#     def on_modified_async(self):
#         print_id_vel('on_modified_async', self.view)

#     def on_selection_modified(self):
#         print_id_vel('on_selection_modified', self.view)

#     def on_selection_modified_async(self):
#         print_id_vel('on_selection_modified_async', self.view)

#     def on_activated(self):
#         print_id_vel('on_activated', self.view)

#     def on_activated_async(self):
#         print_id_vel('on_activated_async', self.view)

#     def on_deactivated(self):
#         print_id_vel('on_deactivated', self.view)

#     def on_deactivated_async(self):
#         print_id_vel('on_deactivated_async', self.view)

#     def on_hover(self, point, hover_zone):
#         print_id_vel('on_hover', self.view)

#     def on_query_context(self, key, operator, operand, match_all):
#         print_id_vel('on_query_context', self.view)

#     def on_query_completions(self, prefix, locations):
#         print_id_vel('on_query_completions', self.view)

#     def on_text_command(self, command_name, args):
#         print_id_vel('on_text_command', self.view)

#     def on_post_text_command(self, command_name, args):
#         print_id_vel('on_post_text_command', self.view)


