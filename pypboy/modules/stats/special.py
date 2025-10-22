import pypboy
import pygame
import game
import config

class Module(pypboy.SubModule):
    label = "S.P.E.C.I.A.L."
    
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        
        # Add your module initialization code here
        # For example:
        # self.special_list = []
        # self.setup_ui()