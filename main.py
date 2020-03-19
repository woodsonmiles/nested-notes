#!/usr/bin/python3
from model import Model
from view import View
from curses import wrapper
from controller import Controller


def main(window):
    view = View(window)
    model = Model(view)
    controller: Controller = Controller(model)
    controller.run()


if __name__ == '__main__':
    wrapper(main)
