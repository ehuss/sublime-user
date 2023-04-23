import os
import re
import subprocess
import sublime
import sublime_plugin
import webbrowser

import sublime, sublime_plugin

class SelectAllSpellingErrorsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = []
        while True:
            self.view.run_command('next_misspelling')
            if self.view.sel()[0] not in regions:
                regions.append(self.view.sel()[0])
            else:
                break
        self.view.sel().clear()
        self.view.sel().add_all(regions)


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


class EricGithubView(sublime_plugin.WindowCommand):

    def run(self, command='blame', branch=None):
        view = self.window.active_view()
        if not view:
            return
        file_name = view.file_name()
        if not file_name:
            return
        dirpath = os.path.dirname(file_name)
        repo_relative_path = git(['git', 'ls-files', '--full-name', file_name], dirpath)

        upstream_url = remote_url('upstream', dirpath)
        origin_url = remote_url('origin', dirpath)
        if not origin_url:
            sublime.error_message('Could not determine origin URL.')
            return
        local_branch_name = git(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], dirpath)
        remote_branch_name = None
        remote_base = None
        # Check if branch exists on upstream, use that if available.
        if upstream_url:
            try:
                git(['git', 'rev-parse', 'refs/remotes/upstream/%s' % (local_branch_name)], dirpath)
                remote_branch_name = local_branch_name
                remote_base = upstream_url
            except subprocess.CalledProcessError:
                pass
        if not remote_branch_name:
            # Check if branch is available in origin.
            try:
                actual_origin_branch = git(['git', 'rev-parse', '--abbrev-ref', '@{u}'], dirpath)
                assert actual_origin_branch.startswith('origin/')
                remote_branch_name = actual_origin_branch[7:]
                remote_base = origin_url
            except subprocess.CalledProcessError:
                pass
        if not remote_branch_name:
            # Fall back to master.
            remote_branch_name = 'master'
            if upstream_url:
                remote_base = upstream_url
            else:
                remote_base = origin_url
        if branch != None:
            # Let the caller override it.
            remote_branch_name = branch
            if upstream_url:
                remote_base = upstream_url
            else:
                remote_base = origin_url

        line = view.rowcol(view.sel()[0].begin())[0] + 1
        to_open = '%s/%s/%s/%s#L%i' % (remote_base, command, remote_branch_name, repo_relative_path, line)
        print('open %r' % (to_open,))
        webbrowser.open(to_open)


def remote_url(remote, path):
    try:
        url = git(['git', 'config', '--get', 'remote.%s.url' % (remote,)], path)
    except subprocess.CalledProcessError:
        return None
    m = re.match(r'git@github.com:(.*?)(?:\.git)?$', url)
    if m:
        return 'https://github.com/%s' % (m.group(1),)
    else:
        m = re.match(r'(https://github.com/.*?)(?:\.git)?$', url)
        if m:
            return m.group(1)
        else:
            sublime.error('Unrecognized remote: %s' % (url,))
            return None


def git(command, path):
    return subprocess.check_output(command,
        cwd=path, universal_newlines=True).strip()


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


