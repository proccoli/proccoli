import os

from Process import Process
from Palette import palette
from urwid import (
    ListBox,
    SimpleFocusListWalker,
    MainLoop,
    ExitMainLoop
)

PROC_DIR = '/proc'

class ProcessListWalker(SimpleFocusListWalker):
    process_dict = {} # check if process already exists in O(1)
    process_list = []

    at_top = True
    sort_var = 'cpu_perc'
    asc=True
    def __init__ (self, w=(12, 8, 15, 10, 10, 10, 15)):
        """
            @method __init__
            Initializes the widgets
        """
        self.w = w
        super(ProcessListWalker, self).__init__(self.process_list)
        self.update()
    def update (self):
        """
            @method update
            Finds new processes by use of memoization
            Iteratively updates or creates an entry for
            processes
        """
        pids = [int(pid) for pid in os.listdir(PROC_DIR) if pid.isdigit()]
        for pid in pids:
            if pid in self.process_dict: # it already exists
                self.process_dict[pid].update()
            else:
                p = Process(pid, self.item_focus, self.item_remove, self.w)
                self.process_dict[pid] = p
                self.append(p)
        self.sort(key = lambda x: getattr(x, self.sort_var), reverse=self.asc)
        if self.at_top:
            self.set_focus(0)
    def item_focus (self, obj):
        """
            @method item_focus
            @param obj
                Either
                    an instance of a Process
                    letter repr a keypress

            Maintains at_top, by parsing actions
            propogated up from the individual processes.
        """
        if isinstance(obj, Process):
            self.at_top = self.index(obj) is 0
            return
        key = obj
        if key is 'up':
            self.at_top = self.focus is 0
        elif key is 'down':
            self.at_top = False
    def item_remove(self, o):
        self.remove(o)
    def set_sort(self, s='cpu_perc', asc=True):
        self.sort_var = s
        self.asc = asc
"""
    Testing
"""
if __name__ == '__main__':
    pl = ProcessListWalker()
    lb = ListBox(pl)
    def exit (p):
        if p is 'q':
            raise ExitMainLoop()
    def refresh(loop, data):
        pl.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(lb, palette=palette, pop_ups=True, unhandled_input=exit)
    main_loop.set_alarm_in(1, refresh)

    main_loop.run()
