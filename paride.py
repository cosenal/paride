import sublime
import sublime_plugin
import random
from itertools import cycle

class NewGameCommand(sublime_plugin.WindowCommand):

    roles = [
        'Werewolf',
        'Werewolf',
        'Veggente',
        'Indemoniato',
    ]

    def create_sheet(self, n):
        n = int(n)
        if n < 6:
            sublime.error_message("Too few players :(")
            return
        view = self.window.new_file()
        all_roles = self.roles + ['Peasant'] * (n - len(self.roles)) 
        shuffle = random.sample(all_roles, len(all_roles))
        text = " : " + "\n : ".join(shuffle)
        view.run_command("fill_roles", {"textBuffer": text})

    def run(self):
        self.window.show_input_panel("How many players?", "", self.create_sheet, None, None)


class FillRolesCommand(sublime_plugin.TextCommand):
    def run(self, edit, textBuffer):
        self.view.insert(edit, 0, textBuffer)
        pt = self.view.text_point(0, 0)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))

        self.view.show(pt)


class StartGameCommand(sublime_plugin.WindowCommand):
    
    mantra = [
        "It's night. Everybody close your eyes.",
        "Werewolves, open your eyes.",
        "Werewolves, pick someone to kill.",
        "Werewolves, close your eyes.",
        "Veggente, open your eyes. Veggente, pick someone to ask about.",
        "Veggente, close your eyes.",
        "Everybody open your eyes; it's daytime."
    ]

    def run(self):
        for s in cycle(self.mantra):
            if not sublime.ok_cancel_dialog(s, 'next'):
                break