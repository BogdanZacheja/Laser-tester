import re
import matplotlib.pyplot as plt


def plot_file(file: str):
    """
    Function to read coordinates from a G-code file and use it to create a plot with the tool path.

    Parameters
    ----------
    file : str
        Name of the G-code file to read.
    """
    x_position = [0]
    y_position = [0]
    z_position = [0]

    with open(file, "r") as file:
        def write_positions(column, position, position_dot):
            if not position and not position_dot:
                column.append(column[-1])
            elif not position_dot:
                column.append(float(position[0]))
            else:
                column.append(float(position_dot[0]))

        for line in file:
            resultx = re.findall(r'X(\d+\.?\d*)', line)
            resulty = re.findall(r'Y(\d+\.?\d*)', line)
            resultz = re.findall(r'Z(\d+\.?\d*)', line)

            write_positions(x_position, resultx, resultx)
            write_positions(y_position, resulty, resulty)
            write_positions(z_position, resultz, resultz)

    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_position, y_position, z_position)
    plt.show()
