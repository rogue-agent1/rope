#!/usr/bin/env python3
"""rope - Rope data structure for efficient string editing."""
import sys

class RopeNode:
    def __init__(self, text=None, left=None, right=None):
        if text is not None:
            self.text = text
            self.weight = len(text)
            self.left = None
            self.right = None
        else:
            self.text = None
            self.left = left
            self.right = right
            self.weight = _length(left)

def _length(node):
    if not node:
        return 0
    if node.text is not None:
        return len(node.text)
    return _length(node.left) + _length(node.right)

def concat(a, b):
    if not a:
        return b
    if not b:
        return a
    return RopeNode(left=a, right=b)

def index(node, i):
    if node.text is not None:
        return node.text[i]
    if i < node.weight:
        return index(node.left, i)
    return index(node.right, i - node.weight)

def to_string(node):
    if not node:
        return ""
    if node.text is not None:
        return node.text
    return to_string(node.left) + to_string(node.right)

def split(node, i):
    if not node:
        return None, None
    if node.text is not None:
        return (RopeNode(node.text[:i]) if i > 0 else None,
                RopeNode(node.text[i:]) if i < len(node.text) else None)
    if i <= node.weight:
        left_l, left_r = split(node.left, i)
        return left_l, concat(left_r, node.right)
    else:
        right_l, right_r = split(node.right, i - node.weight)
        return concat(node.left, right_l), right_r

def insert(node, i, text):
    left, right = split(node, i)
    return concat(concat(left, RopeNode(text)), right)

def delete(node, i, length):
    left, rest = split(node, i)
    _, right = split(rest, length)
    return concat(left, right)

def test():
    r = RopeNode("Hello, ")
    r = concat(r, RopeNode("World!"))
    assert to_string(r) == "Hello, World!"
    assert _length(r) == 13
    assert index(r, 0) == "H"
    assert index(r, 7) == "W"
    r = insert(r, 7, "Beautiful ")
    assert to_string(r) == "Hello, Beautiful World!"
    r = delete(r, 7, 10)
    assert to_string(r) == "Hello, World!"
    left, right = split(r, 5)
    assert to_string(left) == "Hello"
    assert to_string(right) == ", World!"
    print("OK: rope")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: rope.py test")
