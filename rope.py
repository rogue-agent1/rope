#!/usr/bin/env python3
"""Rope data structure — efficient string manipulation for text editors."""
import sys

class RopeNode:
    def __init__(self, text=None, left=None, right=None):
        if text is not None:
            self.text = text; self.left = self.right = None
            self.weight = len(text); self.length = len(text)
        else:
            self.text = None; self.left = left; self.right = right
            self.weight = left.length if left else 0
            self.length = (left.length if left else 0) + (right.length if right else 0)

class Rope:
    LEAF_SIZE = 32
    def __init__(self, text=""):
        self.root = self._build(text) if text else None
    def _build(self, text):
        if len(text) <= self.LEAF_SIZE:
            return RopeNode(text=text)
        mid = len(text) // 2
        return RopeNode(left=self._build(text[:mid]), right=self._build(text[mid:]))
    def __len__(self):
        return self.root.length if self.root else 0
    def index(self, i, node=None):
        if node is None: node = self.root
        if node.text is not None: return node.text[i]
        if i < node.weight: return self.index(i, node.left)
        return self.index(i - node.weight, node.right)
    def __getitem__(self, i):
        if i < 0: i += len(self)
        return self.index(i)
    def concat(self, other):
        r = Rope()
        r.root = RopeNode(left=self.root, right=other.root)
        return r
    def split(self, i, node=None):
        if node is None: node = self.root
        if node.text is not None:
            l, r = Rope(), Rope()
            l.root = RopeNode(text=node.text[:i])
            r.root = RopeNode(text=node.text[i:])
            return l, r
        if i <= node.weight:
            ll, lr = self.split(i, node.left)
            rr = Rope(); rr.root = RopeNode(left=lr.root, right=node.right)
            return ll, rr
        rl, rr = self.split(i - node.weight, node.right)
        ll = Rope(); ll.root = RopeNode(left=node.left, right=rl.root)
        return ll, rr
    def insert(self, i, text):
        l, r = self.split(i)
        m = Rope(text)
        return l.concat(m).concat(r)
    def delete(self, i, length):
        l, rest = self.split(i)
        _, r = rest.split(length)
        return l.concat(r)
    def to_string(self, node=None):
        if node is None: node = self.root
        if node is None: return ""
        if node.text is not None: return node.text
        return self.to_string(node.left) + self.to_string(node.right)
    def __str__(self): return self.to_string()
    def _depth(self, node=None):
        if node is None: node = self.root
        if node is None or node.text is not None: return 0
        return 1 + max(self._depth(node.left) if node.left else 0,
                       self._depth(node.right) if node.right else 0)

if __name__ == "__main__":
    r = Rope("Hello, World! This is a rope data structure for efficient text editing.")
    print(f"Original ({len(r)} chars, depth {r._depth()}): {r}")
    r = r.insert(7, "Beautiful ")
    print(f"Insert   ({len(r)} chars): {r}")
    r = r.delete(7, 10)
    print(f"Delete   ({len(r)} chars): {r}")
    a, b = r.split(13)
    print(f"Split at 13: '{a}' | '{b}'")
    big = Rope("x" * 10000)
    big = big.insert(5000, "INSERTED")
    print(f"\nBig rope: {len(big)} chars, depth {big._depth()}, char[5002]={big[5002]!r}")
