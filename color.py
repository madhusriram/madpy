def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

print_format_table()

# color table:
# Intensity:    0     1   2     3      4    5       6    7 
# Normal:       Black Red Green Yellow Blue Magenta Cyan White 
# Bright:       Black Red Green Yellow Blue Magenta Cyan White

# Foreground, add 30 to the color table
# Backgroud, add 40 to the color table
