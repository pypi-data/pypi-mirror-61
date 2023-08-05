# McStasScript
McStas API for creating and running McStas instruments from python scripting

Prototype for an API that allow interaction with McStas through an interface like Jupyter Notebooks created under WP5 of PaNOSC.

## Instructions for basic use:
Download the entire project

Set up paths to McStas in the configuration.yaml file

Before import in python, add the project to your path: 

    import sys
    sys.path.append('path/to/McStasScript')

Import the interface 

    from mcstasscript.interface import instr, plotter, functions

Now the package can be used. Start with creating a new instrument, just needs a name

    my_instrument = instr.McStas_instr("my_instrument_file")

Then McStas components can be added, here we add a source

    my_source = my_instrument.add_component("source", "Source_simple")
    my_source.show_parameters() # Can be used to show available parameters for Source simple

The parameters of the source can be adjusted directly as attributes of the python object

    my_source.xwidth = 0.12
    my_source.yheight = 0.12
    my_source.lambda0 = 3
    my_source.dlambda = 2.2
    my_source.focus_xw = 0.05
    my_source.focus_yh = 0.05
    
A monitor is added as well to get data out of the simulation

    PSD = Instr.add_component("PSD", "PSD_monitor", AT=[0,0,1], RELATIVE="source") 
    PSD.xwidth = 0.1
    PSD.yheight = 0.1
    PSD.nx = 200
    PSD.ny = 200
    PSD.filename = "\"PSD.dat\""

This simple simulation can be executed from the 

    data = my_instrument.run_full_instrument(foldername="first_run", increment_folder_name=True)

Results from the monitors would be stored as a list of McStasData objects in the returned data. The counts are stored as numpy arrays. We can read and change the intensity directly and manipulate the data before plotting.

    data[0].Intensity
    
Plotting is usually done in a subplot of all monitors recorded.    

    plot = plotter.make_sub_plot(data)


## Method overview
Here is a quick overview of the available methods of the main classes in the project. Most have more options from keyword arguments that are explained in the manual, but also in python help, for example help(instr.McStas_instr.show_components).

    instr
    └── McStas_instr(str instr_name) # Returns McStas instrument object on initialize
        ├── show_components(str category_name) # Show available components in given category
        ├── component_help(str component_name) # Prints component parameters for given component name   
        ├── add_component(str name, str component_name) # Adds component to instrument and returns object
        ├── add_parameter(str name) # Adds instrument parameter with name
        ├── add_declare_var(str type, str name) # Adds declared variable with type and name
        ├── append_initialize(str string) # Appends a line to initialize (c syntax)
        ├── print_components() # Prints list of components and their location
        ├── write_full_instrument() # Writes instrument to disk with given name + ".instr"
        └── run_full_instrument() # Runs simulation. Options in keyword arguments. Returns list of McStasData
        
    component # returned by add_component
    ├── set_AT(list at_list) # Sets component position (list of x,y,z positions in [m])
    ├── set_ROTATED(list rotated_list) # Sets component rotation (list of x,y,z rotations in [deg])
    ├── set_RELATIVE(str component_name) # Sets relative to other component name
    ├── set_parameters(dict input) # Set parameters using dict input
    ├── set_comment(str string) # Set comment explaining something about the component
    └── print_long() # Prints currently contained information on component
    
    functions
    ├── name_search(str name, list McStasData) # Returns data set with given name from McStasData list
    ├── name_plot_options(str name, list McStasData, kwargs) # Sends kwargs to dataset with given name
    └── load_data(str foldername) # Loads data from folder with McStas data as McStasData list
    
    plotter
    ├── make_plot(list McStasData) # Plots each data set individually
    └── make_sub_plot(list McStasData) # Plots data as subplot
