import sys, getopt
import time

# By default I want the real input, and *not* to debug.
ARG_data = 'input.txt'
ARG_debugLogging = False

# Get the args off the command-line
opts, args = getopt.getopt(sys.argv[1:],"td",["test","debug"])
for opt, arg in opts:
    if opt in ("-t", "--test"):
        print(f"\33[31mUSING TEST DATA\33[0m")
        ARG_data = 'test.txt'
    elif opt in ("-d", "--debug"):
        ARG_debugLogging = True

# Useful during testing to see what the hell is going on
def debug(thing):
    if ARG_debugLogging:
        print(f"\33[39mDEBUG:\33[0m {thing}")

answer_p1 = 0
answer_p2 = 0

#INPUT
import re
from math import gcd
machines_raw = open(ARG_data).read().split('\n\n')

machines = []
for mr in machines_raw:
    a, b, p = mr.split('\n')

    a = re.match(r'Button A: X\+(\d+), Y\+(\d+)', a).groups()
    b = re.match(r'Button B: X\+(\d+), Y\+(\d+)', b).groups()
    p = re.match(r'Prize: X=(\d+), Y=(\d+)', p).groups()
    m = {
        "a": tuple(map(int, a)),
        "b": tuple(map(int, b)),
        "p": tuple(map(int, p)),
    }
    m["p2"] = (m["p"][0] + 10000000000000, m["p"][1] + 10000000000000)

    machines.append(m)

for m in machines:
    ax_ay = m["a"][0] * m["a"][1]
    bx_ay = m["b"][0] * m["a"][1]
    px_ay = m["p"][0] * m["a"][1]
    p2x_ay = (m["p2"][0]) * m["a"][1]
    debug(f"{ax_ay=}, {bx_ay=}, {px_ay=}")

    ay_ax = m["a"][1] * m["a"][0]
    by_ax = m["b"][1] * m["a"][0]
    py_ax = m["p"][1] * m["a"][0]
    p2y_ax = (m["p2"][1]) * m["a"][0]
    debug(f"{ay_ax=}, {by_ax=}, {py_ax=}")

    debug(f"{(by_ax - bx_ay)=}, {(py_ax - px_ay)=}")

    b_presses = (py_ax - px_ay) / (by_ax - bx_ay)
    b2_presses = (p2y_ax - p2x_ay) / (by_ax - bx_ay)
    debug(f"{b_presses=}, {b_presses.is_integer()=}")


    bx_a = m["b"][0] * b_presses
    bx_a2 = m["b"][0] * b2_presses
    a_presses = (m["p"][0] - bx_a) / m["a"][0]
    a2_presses = (m["p2"][0] - bx_a2) / m["a"][0]
    debug(f"{a_presses=}, {a_presses.is_integer()=}")

    if a_presses.is_integer() and b_presses.is_integer():
        answer_p1 += b_presses + a_presses * 3 

    if a2_presses.is_integer() and b2_presses.is_integer():
        answer_p2 += b2_presses + a2_presses * 3 


# Print out the answers
print(f"\33[32m__P1__: \33[1m{int(answer_p1)}\33[0m")
print(f"\33[32m__P2__: \33[1m{int(answer_p2)}\33[0m")

# Tell me how inefficecient my code is
print(f"\33[35mTook \33[1;35m{time.process_time_ns() / 1000000000}\33[0m\33[35m seconds to run\33[0m")


# You want to reach a point (Prize) whose coordinates are given by `X=8400` and `Y=5400`. You can move towards this point by pressing two buttons that move a pointer:

# - Button A moves the pointer by `X+94` and `Y+34` for each press.
# - Button B moves the pointer by `X+22` and `Y+67` for each press.

# To find how many times you need to press each button, let's set up a system of equations where `a` is the number of times you press Button A and `b` is the number of times you press Button B:

# ```
# 94a + 22b = 8400  (Equation 1: X-coordinates)
# 34a + 67b = 5400  (Equation 2: Y-coordinates)
# ```

# To solve this system of equations, you can use methods like substitution or elimination. I'll use the elimination method:

# 1. Multiply Equation 1 by 34 and Equation 2 by 94 (we choose these numbers based on the coefficients of `a` in the original equations) to eliminate variable `a`:

# ```
# 3196a + 748b = 285600  (Equation 1)
# 3196a + 6298b = 507600  (Equation 2)
# ```

# 2. Subtract Equation 1 from Equation 2 to eliminate `a`:

# ```
# 6298b - 748b = 507600 - 285600
# 5550b = 222000
# ```

# 3. Solve for `b`:

# ```
# b = 222000 / 5550
# b = 40
# ```

# 4. Substitute the value of `b` into Equation 1 to find `a`:

# ```
# 94a + 22*40 = 8400
# 94a + 880 = 8400
# 94a = 8400 - 880
# 94a = 7520
# ```

# ```
# a = 7520 / 94
# a = 80
# ```

# Therefore, you need to press Button A `80` times and Button B `40` times to reach the X and Y coordinates of the Prize.