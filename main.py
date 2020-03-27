#!/usr/bin/python3
from model import Model
from linuxView import LinuxView
from curses import wrapper
from controller import Controller


def main(window):
    view = LinuxView(window)
    model = Model(view)
    controller: Controller = Controller(model)
    controller.run()


if __name__ == '__main__':
    wrapper(main)
