"""
Stylors

Build Colors/Styles in ASCII
    from quick_tools.stylors import *
    print(f'{br}{ld}  red_color  {nn} None')

"""

# Build Colors/Styles

# None
nn = "\033[m"

# Styles
sh = "\033[8m"   # Hide
sbl = "\033[5m"  # Blink
sng = "\033[7m"  # Negative

sb = "\033[1m"   # Bold
si = "\033[3m"   # Italic
su = "\033[4m"   # Underline
ss = "\033[9m"   # Scratched

# Colors
cw = "\033[30m"  # White
cr = "\033[31m"  # Red
cg = "\033[32m"  # Green
co = "\033[33m"  # Orange
cb = "\033[34m"  # Blue
cp = "\033[35m"  # Purple
cc = "\033[36m"  # Cyan
cd = "\033[37m"  # Dark

# Light Colors
lw = "\033[90m"  # White
lr = "\033[91m"  # Red
lg = "\033[92m"  # Green
lo = "\033[93m"  # Orange
lb = "\033[94m"  # Blue
lp = "\033[95m"  # Purple
lc = "\033[96m"  # Cyan
ld = "\033[97m"  # Dark

# Background Colors
bw = "\033[40m"  # White
br = "\033[41m"  # Red
bg = "\033[42m"  # Green
bo = "\033[43m"  # Orange
bb = "\033[44m"  # Blue
bp = "\033[45m"  # Purple
bc = "\033[46m"  # Cyan
bd = "\033[47m"  # Dark
