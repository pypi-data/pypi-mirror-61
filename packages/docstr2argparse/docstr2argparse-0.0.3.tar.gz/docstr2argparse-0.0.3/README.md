# Turn a docstring to argparse arguments.

This reduces the boilerplate for automatically creating command line scripts with python.
Probably other projects like this exist, but this one is small.
Right now we only support google style of documentation, which is compatible with using Spinx with its extension: the Napoleon module.

# How it works?

Consider this function with a long long description:
```{python}
def apex3d(raw_folder,
           output_dir,
           lock_mass_z2=785.8426,
           lock_mass_tol_amu=.25,
           low_energy_thr=300,
           high_energy_thr=30,
           lowest_intensity_thr=750,
           write_xml=True,
           write_binary=True,
           write_csv=False,
           max_used_cores=1,
           path_to_apex3d='C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe',
           PLGS=True,
           cuda=True,
           unsupported_gpu=True,
           debug=False,
           **kwds):
    """A wrapper around the infamous Apex3D.
    
    It wraps in Python what would otherwise had to be called with a batch script.

    Args:
        raw_folder (str): a path to the input folder with raw Waters data.
        output_dir (str): Path to where to place the output.
        lock_mass_z2 (float): The lock mass for doubly charged ion (which one, dunno, but I guess a very important one).
        lock_mass_tol_amu (float): Tolerance around lock mass (in atomic mass units, amu).
        low_energy_thr (int): The minimal intensity of a precursor ion so that it ain't a noise peak.
        high_energy_thr (int): The minimal intensity of a fragment ion so that it ain't a noise peak.
        lowest_intensity_thr (int): The minimal intensity of a peak to be analyzed.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the output in a csv in the output folder (doesn't work).
        max_used_cores (int): The maximal number of cores to use.
        path_to_apex3d (str): Path to the "Apex3D.exe" executable.
        PLGS (boolean): No idea what it is.
        cuda (boolean): Use CUDA.
        unsupported_gpu (boolean): Try using an unsupported GPU for calculations. If it doesn't work, the pipeline switches to CPU which is usually much slower.
        debug (boolean): Debug mode.
        kwds: other parameters for 'subprocess.run'.
    
    Returns:
        tuple: the path to the outcome (no extension: choose it yourself and believe more in capitalism) and the completed process.
    """
    pass
```

Our module helps to automatically parse the function signature and documentation and make it ready to be used with the `argparse` module.

Look:
```{python}
from docstr2argparse import foo2argparse

pprint(foo2argparse(apex3d))
```
gives:
```{bash}
In [197]: pprint(foo2argparse(apex3d))                                   
('Analyze a Waters Raw Folder with Apex3D.',                             
 [('--PLGS', {'default': True, 'help': 'No idea what it is. [default: True].'}),
  ('--cuda', {'default': True, 'help': 'Use CUDA. [default: True].'}),
  ('--high_energy_thr',
   {'default': 30,
    'help': "The minimal intensity of a fragment ion so that it ain't a noise "
            'peak. [default: 30].',
    'type': <class 'int'>}),
  ('--lock_mass_tol_amu',
   {'default': 0.25,
    'help': 'Tolerance around lock mass (in atomic mass units, amu). [default: '
            '0.25].',
    'type': <class 'float'>}),
  ('--lock_mass_z2',
   {'default': 785.8426,
    'help': 'The lock mass for doubly charged ion. [default: 785.8426].',
    'type': <class 'float'>}),
  ('--low_energy_thr',
   {'default': 300,
    'help': "The minimal intensity of a precursor ion so that it ain't a noise "
            'peak. [default: 300].',
    'type': <class 'int'>}),
  ('--lowest_intensity_thr',
   {'default': 750,
    'help': 'The minimal intensity of a peak to be analyzed. [default: 750].',
    'type': <class 'int'>}),
  ('--max_used_cores',
   {'default': 8,
    'help': 'The maximal number of cores to use. [default: 8].',
    'type': <class 'int'>}),
  ('output_dir',
   {'help': 'Path to where to place the output.', 'type': <class 'str'>}),
  ('--path_to_apex3d',
   {'default': 'C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe',
    'help': 'Path to the "Apex3D.exe" executable. [default: '
            'C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe].',
    'type': <class 'str'>}),
  ('raw_folder',
   {'help': 'a path to the input folder with raw Waters data.',
    'type': <class 'str'>}),
  ('--timeout_apex3d',
   {'default': 60,
    'help': 'Timeout in minutes. [default: 60].',
    'type': <class 'float'>}),
  ('--unsupported_gpu',
   {'default': True,
    'help': "Try using an unsupported GPU for calculations. If it doesn't "
            'work, the pipeline switches to CPU which is usually much slower. '
            '[default: True].'}),
  ('--write_binary',
   {'default': True,
    'help': 'Write the binary output in an xml in the output folder. [default: '
            'True].'}),
  ('--write_csv',
   {'default': False,
    'help': "Write the output in a csv in the output folder (doesn't work). "
            '[default: False].'}),
  ('--write_xml',
   {'default': False,
    'help': 'Write the output in an xml in the output folder. [default: '
            'False].'})])
```

Neet. But that's not all folks.

```{python}
from docstr2argparse import document

document(apex3d).print_help()
```
generates the almighty help:
```{bash}
usage: ipython3 [-h] [--PLGS PLGS] [--cuda CUDA]                         
                [--high_energy_thr HIGH_ENERGY_THR]
                [--lock_mass_tol_amu LOCK_MASS_TOL_AMU]
                [--lock_mass_z2 LOCK_MASS_Z2]
                [--low_energy_thr LOW_ENERGY_THR]
                [--lowest_intensity_thr LOWEST_INTENSITY_THR]
                [--max_used_cores MAX_USED_CORES]
                [--path_to_apex3d PATH_TO_APEX3D]
                [--timeout_apex3d TIMEOUT_APEX3D]
                [--unsupported_gpu UNSUPPORTED_GPU]
                [--write_binary WRITE_BINARY] [--write_csv WRITE_CSV]
                [--write_xml WRITE_XML]
                output_dir raw_folder

Analyze a Waters Raw Folder with Apex3D.

positional arguments:
  output_dir            Path to where to place the output.
  raw_folder            a path to the input folder with raw Waters data.

optional arguments:
  -h, --help            show this help message and exit
  --PLGS PLGS           No idea what it is. [default: True].
  --cuda CUDA           Use CUDA. [default: True].
  --high_energy_thr HIGH_ENERGY_THR
                        The minimal intensity of a fragment ion so that it
                        ain't a noise peak. [default: 30].
  --lock_mass_tol_amu LOCK_MASS_TOL_AMU
                        Tolerance around lock mass (in atomic mass units,
                        amu). [default: 0.25].
  --lock_mass_z2 LOCK_MASS_Z2
                        The lock mass for doubly charged ion. [default:
                        785.8426].
  --low_energy_thr LOW_ENERGY_THR
                        The minimal intensity of a precursor ion so that it
                        ain't a noise peak. [default: 300].
  --lowest_intensity_thr LOWEST_INTENSITY_THR
                        The minimal intensity of a peak to be analyzed.
                        [default: 750].
  --max_used_cores MAX_USED_CORES
                        The maximal number of cores to use. [default: 8].
  --path_to_apex3d PATH_TO_APEX3D
                        Path to the "Apex3D.exe" executable. [default:
                        C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe].
  --timeout_apex3d TIMEOUT_APEX3D
                        Timeout in minutes. [default: 60].
  --unsupported_gpu UNSUPPORTED_GPU
                        Try using an unsupported GPU for calculations. If it
                        doesn't work, the pipeline switches to CPU which is
                        usually much slower. [default: True].
  --write_binary WRITE_BINARY
                        Write the binary output in an xml in the output
                        folder. [default: True].
  --write_csv WRITE_CSV
                        Write the output in a csv in the output folder
                        (doesn't work). [default: False].
  --write_xml WRITE_XML
                        Write the output in an xml in the output folder.
                        [default: False].
```


# Installation
It should work under both Pythons, but use Python3 just to make Michał Startek feel old and useless.
```{bash}
pip3 install docstr2argparse
```