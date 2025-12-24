import tempfile
import shutil
import os
from IPython.display import display, SVG
import ipywidgets as widgets
from nopm.figure import Figure

class FigureCreator:
    def __init__(self, figure: Figure):
        self.figure = figure

    def generate(self, description: str, file_name: str, n_options: int = 3):
        options = []
        for i in range(n_options):
            # Create a temporary file for each option
            # We use a context manager to ensure the file is closed, but we keep the path
            # We don't delete immediately because we need it for display and selection
            fd, path = tempfile.mkstemp(suffix=".svg")
            os.close(fd)
            
            # Generate the SVG
            print("Generating option number %d..." % (i+1))
            self.figure.generate(description, path)
            options.append(path)

        # Display options in rows of 3 (side-by-side)
        option_widgets = []
        for i, path in enumerate(options):
            with open(path, 'r', encoding='utf-8') as f:
                svg = f.read()

            # Wrap SVG in an HTML widget so it can be placed inside ipywidgets layout
            # Ensure the SVG scales to the container: max-width:100% and height:auto
            html = widgets.HTML(value=(
                f'<div style="width:100%;display:flex;justify-content:center;align-items:center;overflow:hidden;">'
                f'<div style="width:100%;">'
                f'<style>svg{{max-width:100%;height:auto;display:block}}</style>'
                f'{svg}'
                f'</div></div>'
            ))
            label = widgets.Label(value=f"Option {i+1}")

            # Each option is a vertical box (image above label) and takes ~1/3 width
            option_box = widgets.VBox([
                html,
                label
            ], layout=widgets.Layout(align_items='center', width='33%', min_width='0'))
            option_widgets.append(option_box)

        # Group option boxes into rows of 3
        rows = []
        for i in range(0, len(option_widgets), 3):
            row_children = option_widgets[i:i+3]
            row = widgets.HBox(row_children, layout=widgets.Layout(justify_content='flex-start', width='100%'))
            rows.append(row)

        display(widgets.VBox(rows))

        # Create ToggleButtons
        toggles = widgets.ToggleButtons(
            options=[(f'Option {i+1}', i) for i in range(len(options))],
            description='Select Figure:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
        )

        # Create Select Button
        select_button = widgets.Button(
            description='Select',
            disabled=False,
            button_style='success', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Save selected figure to disk',
            icon='check'
        )

        output = widgets.Output()

        def on_button_clicked(b):
            with output:
                selected_index = toggles.value
                selected_path = options[selected_index]
                shutil.copy(selected_path, file_name)
                print(f"Selected Option {selected_index+1} saved to {file_name}")
                
                # Cleanup temp files? 
                # Ideally we would clean up, but maybe keep them for the session?
                # For this implementation, we'll leave them as temp files are usually cleaned up by OS eventually or user can restart kernel.
        
        select_button.on_click(on_button_clicked)
        
        display(toggles, select_button, output)
