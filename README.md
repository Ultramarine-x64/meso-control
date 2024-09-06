# Master-dissertation
The work is devoted to clustering in multi-agent systems

### Install dependencies
- Use python 3.11
- From root:
```
pip install -r ./requirements.txt
```

### How to use with application
- From root:
```
python application.py
```
- The repository contains the configuration of simulation for example `/configurations/test_configuration.json`

### How to use with cmd
- From root:
```
python main.py
```
- The repository contains the configuration of simulation for example `/configurations/test_configuration.json`
- You can enter flags:
	- `--configuration_file=relative/path/to/file`
	- `--path_to_results=relative/path/to/results/folder`
	- `--create_result_graph=True`
	- `--create_step_images=True`
	- `--create_gif=True`
	- `--gif_duration=10`
