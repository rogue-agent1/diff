#!/usr/bin/env python3
"""diff — Myers diff algorithm with unified diff output. Zero deps."""
import sys

def myers_diff(a, b):
    n, m = len(a), len(b)
    max_d = n + m
    v = {1: 0}
    trace = []
    for d in range(max_d + 1):
        trace.append(dict(v))
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v.get(k-1, -1) < v.get(k+1, -1)):
                x = v.get(k+1, 0)
            else:
                x = v.get(k-1, 0) + 1
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x += 1; y += 1
            v[k] = x
            if x >= n and y >= m:
                return _backtrack(trace, a, b, n, m)
    return []

def _backtrack(trace, a, b, n, m):
    x, y = n, m
    edits = []
    for d in range(len(trace) - 1, 0, -1):
        v = trace[d - 1]
        k = x - y
        if k == -d or (k != d and v.get(k-1, -1) < v.get(k+1, -1)):
            prev_k = k + 1
        else:
            prev_k = k - 1
        prev_x = v.get(prev_k, 0)
        prev_y = prev_x - prev_k
        while x > prev_x and y > prev_y:
            edits.append((' ', a[x-1]))
            x -= 1; y -= 1
        if d > 0:
            if x == prev_x:
                edits.append(('+', b[y-1]))
                y -= 1
            else:
                edits.append(('-', a[x-1]))
                x -= 1
    while x > 0 and y > 0:
        edits.append((' ', a[x-1]))
        x -= 1; y -= 1
    edits.reverse()
    return edits

def unified_diff(a_lines, b_lines, a_name="a", b_name="b", context=3):
    edits = myers_diff(a_lines, b_lines)
    if all(op == ' ' for op, _ in edits):
        return ""
    lines = [f"--- {a_name}", f"+++ {b_name}"]
    for op, line in edits:
        prefix = ' ' if op == ' ' else op
        lines.append(f"{prefix}{line}")
    return '\n'.join(lines)

def main():
    if len(sys.argv) == 3:
        with open(sys.argv[1]) as f: a = f.readlines()
        with open(sys.argv[2]) as f: b = f.readlines()
        a = [l.rstrip('\n') for l in a]
        b = [l.rstrip('\n') for l in b]
        print(unified_diff(a, b, sys.argv[1], sys.argv[2]))
    else:
        a = ["The", "quick", "brown", "fox", "jumps"]
        b = ["The", "slow", "brown", "fox", "leaps", "high"]
        print("Diff:")
        edits = myers_diff(a, b)
        for op, word in edits:
            print(f"  {op} {word}")
        print(f"\nUnified:\n{unified_diff(a, b)}")

if __name__ == "__main__":
    main()
