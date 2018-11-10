import sublime
import sublime_plugin
import os
import subprocess


class EricNewRustProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if self.window.project_file_name() is not None:
            sublime.error_message('This window already has a project.')
            return
        if len(self.window.folders()) == 0:
            sublime.error_message('Add folders before running.')
            return
        if len(self.window.folders()) != 1:
            # TODO: UI to pick one
            sublime.error_message('Too many folders.')
            return
        for view in self.window.views():
            if view.is_dirty():
                sublime.error_message('Save all views before running.')
                return
        project = """
{
    "folders":
    [
        {
            "path": ".",
            "folder_exclude_patterns": ["target"]
        }
    ]
}
"""
        folder = self.window.folders()[0]
        name = os.path.basename(folder)
        project_path = os.path.join(self.window.folders()[0], '%s.sublime-project' % (name,))
        if os.path.exists(project_path):
            sublime.error_message('Path %r already exists.' % (project_path,))
            return
        open(project_path, 'w').write(project)
        subl = sublime.executable_path()
        if sublime.platform() == 'osx':
            subl = subl[:subl.rfind(".app/") + 5] + 'Contents/SharedSupport/bin/subl'
        self.window.run_command('close_all')
        self.window.run_command('close_project')
        subprocess.check_call([subl, project_path])
