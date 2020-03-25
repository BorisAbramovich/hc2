from __future__ import absolute_import

from basics import *

logging.info('req')
import requests
logging.info('np')
import numpy as np
logging.info('pandas')
import pandas
logging.info('nx')
import networkx as nx
logging.info('plt')
import matplotlib.pyplot as plt
logging.info('sympy')
import sympy
logging.info('ipython')
from IPython import embed, start_ipython
logging.info('display')
from IPython.display import display
logging.info('socket')
import socket
socket.setdefaulttimeout(5)
del socket

from IPython.core.debugger import Pdb
ipdb = Pdb()
del Pdb

# sympy.init_printing()


def qt_ipdb_trace():
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()
    ipdb.set_trace()


def qt_pdb_trace():
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()
    pdb.set_trace()


def public_ip():
    """Return the internet facing IP returned by http://ipecho.net/plain"""
    return requests.get('http://ipecho.net/plain').text


def single_source_subgraph(g, node):
    """
    Return the sub-graph reachable from node in a `networkx` graph.
    """
    return g.subgraph(nx.single_source_shortest_path(g, node).keys())


def graph_calls(**kwargs):
    """
    A decorator that gives the function the ability to plot a graph of recursive calls.
    Plots the calls based on the first two arguments which should be numbers.
    """
    kwargs.setdefault('pos', dictify(lambda *args: args[:2]))
    kwargs.setdefault('width', 0.2)
    kwargs.setdefault('font_size', 0)
    kwargs.setdefault('node_size', 0)

    def _deco(f):

        import inspect

        real_f = f.__wrapped__ if hasattr(f, '__wrapped__') else f
        arg_names = inspect.getargs(real_f.__code__).args[:2]
        if len(arg_names) < 2:
            arg_names = ['', '']

        call_stack = []

        @functools.wraps(f)
        def _f(*args):
            _f.call_graph.add_node(args)
            if call_stack:
                _f.call_graph.add_edge(call_stack[-1], args)
            call_stack.append(args)
            res = f(*args)
            call_stack.pop()
            return res

        _f.call_graph = nx.DiGraph()

        def draw_call_graph(*args):
            if not args:
                nx.draw_networkx(_f.call_graph, **kwargs)
            else:
                node = kwargs['pos'][args]
                if node not in _f.call_graph:
                    _f(*args)
                nx.draw_networkx(single_source_subgraph(_f.call_graph, node), **kwargs)
            plt.xlabel(arg_names[0])
            plt.ylabel(arg_names[1])

        _f.draw_call_graph = draw_call_graph
        return _f

    return _deco


def sub_rows(arr, sub_size):
    """
    Yield all sub-rows of length `sub_size` in the 2d numpy array `arr`.

    Args:
        arr: A 2d numpy array. ``arr[0, 0]`` is considered the top-left corner.
        sub_size: The length of the sub-rows to yield.

    Yields:
        The sub-rows.
    """
    rows, cols = arr.shape
    for i in range(rows):
        for j in range(cols - sub_size + 1):
            yield arr[i, range(j, j + sub_size)]


def sub_columns(arr, sub_size):
    """
    Yield all sub-columns of length `sub_size` in the 2d numpy array `arr`.

    Args:
        arr: A 2d numpy array. ``arr[0, 0]`` is considered the top-left corner.
        sub_size: The length of the sub-columns to yield.

    Yields:
        The sub-columns.
    """
    return sub_rows(arr.T, sub_size)


def sub_major_diags(arr, sub_size):
    """
    Yield all top-left to bottom-right diagonals of length `sub_size` in the 2d numpy array `arr`.

    Args:
        arr: A 2d numpy array. ``arr[0, 0]`` is considered the top-left corner.
        sub_size: The length of the diagonals to yield.

    Yields:
        The diagonals.
    """
    rows, cols = arr.shape
    for i in range(rows - sub_size + 1):
        for j in range(cols - sub_size + 1):
            yield arr[range(i, i + sub_size), range(j, j + sub_size)]


def sub_minor_diags(arr, sub_size):
    """
    Yield all bottom-left to top-right diagonals of length `sub_size` in the 2d numpy array `arr`.

    Args:
        arr: A 2d numpy array. ``arr[0, 0]`` is considered the top-left corner.
        sub_size: The length of the diagonals to yield.

    Yields:
        The diagonals.
    """
    return sub_major_diags(arr[:, ::-1], sub_size)
