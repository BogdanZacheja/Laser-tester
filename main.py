from tkinter import Tk, Frame, Label, Button, Entry, StringVar, DoubleVar, IntVar, PhotoImage
from tkinter import ttk
from pattern_generator import PatternGenerator


def generate_g_code():
    """
    Retrieve the input values, convert them to appropriate types,
    and generate the G-code using the PatternGenerator.
    """
    try:
        params = {key: fields[key][0].get() for key in fields}
        # Convert appropriate values to float/int as needed
        params['length'] = float(params['length'])
        params['width'] = float(params['width'])
        params['space'] = float(params['space'])
        params['passes_per_mm'] = int(params['passes_per_mm'])
        params['x_start_pos'] = float(params['x_start_pos'])
        params['y_start_pos'] = float(params['y_start_pos'])
        params['x_squares'] = int(params['x_squares'])
        params['y_squares'] = int(params['y_squares'])
        params['start_power'] = int(params['start_power'])
        params['end_power'] = int(params['end_power'])
        params['start_feed'] = int(params['start_feed'])
        params['end_feed'] = int(params['end_feed'])

        generator = PatternGenerator(**params)
        generator.generate_pattern()
        print('G-code generation completed successfully.')

    except ValueError as error:
        print(f'Invalid value in field: {error}')


class ResponsiveApp(Frame):
    """
    A responsive application for generating laser cutting patterns.
    """
    def __init__(self, master):
        super().__init__(master)
        self.grid(sticky="nsew")

        # Configure grid layout to be responsive
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=2)
        master.rowconfigure(0, weight=1)

        # Create frames for image and input
        self.image_frame = Frame(self, width=200, height=400)
        self.input_frame = Frame(self, width=400, height=400)

        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.create_image(self.image_frame)
        self.create_entries(fields, self.input_frame)

    def create_image(self, parent):
        """
        Create and place an image in the specified parent frame.
        """
        self.image = PhotoImage(file="img/instruction.png")
        self.image_label = Label(parent, image=self.image)
        self.image_label.pack(fill="both", expand=True)

    def create_entries(self, fields, parent):
        """
        Create input fields and labels based on the provided fields dictionary.
        """
        for c, i in enumerate(fields):
            cur_label = ttk.Label(parent, text=fields[i][1])
            cur_label.grid(row=c, column=0, sticky='W', padx=5, pady=5)
            cur_entrybox = ttk.Entry(parent, width=20, textvariable=fields[i][0])
            cur_entrybox.grid(column=1, row=c, padx=5, pady=5)
            cur_entrybox.delete(0, 'end')
            cur_entrybox.insert(0, str(fields[i][2]))
        self.button = ttk.Button(parent, text='Generate G-code', command=generate_g_code)
        self.button.grid(row=c + 1, column=0, columnspan=2, pady=10)


if __name__ == '__main__':
    root = Tk()
    root.title('Responsive Laser Pattern Generator')

    fields = {
        'file_name': [StringVar(), 'File name', 'test_laser.nc'],
        'length': [DoubleVar(), 'Square length [mm]', 10.0],
        'width': [DoubleVar(), 'Square width [mm]', 10.0],
        'space': [DoubleVar(), 'Space [mm]', 5.0],
        'passes_per_mm': [IntVar(), 'Passes per mm', 10],
        'x_start_pos': [DoubleVar(), 'Start position X', 0.0],
        'y_start_pos': [DoubleVar(), 'Start position Y', 0.0],
        'x_squares': [IntVar(), 'Number of squares X', 5],
        'y_squares': [IntVar(), 'Number of squares Y', 5],
        'start_power': [IntVar(), 'Start power', 100],
        'end_power': [IntVar(), 'End power', 1000],
        'start_feed': [IntVar(), 'Start feed', 1000],
        'end_feed': [IntVar(), 'End feed', 5000],
        'turn_on_g_code': [StringVar(), 'Turn on G code', 'M4'],
        'turn_off_g_code': [StringVar(), 'Turn off G code', 'M5'],
    }

    app = ResponsiveApp(root)
    root.mainloop()
