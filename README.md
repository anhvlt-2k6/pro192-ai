# OSG AI

Build OSG AI for class submission

Prerequisites:

* Obtain the Operating system knowledge from the text books
* Provide some knowledge to users about operating system of the class OSG
* English is required. Vietnamese is optional.

## Requirements

* An NVIDIA GPU with Studio driver installed and above version 550.
* Minimum available memory (not total memory and exclude swap memory) is 12gb.
* A GNU/Linux operating system that run based-on AMD64 architecture.
* Anaconda (or Miniconda) environment. You can [download from here](https://www.anaconda.com/download).

> Note for WSL2 users:
>
> 1. NVIDIA GPU should not be installed normally within the distro, since installing the actual driver requires the Linux header (`linux-headers`), which is not available in the WSL. Instead, please review [Getting Started with CUDA on WSL 2](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)
> 2. In `.wslconfig`, please enable [GPU settings](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#gpu-settings) (set to `true` or `default`) and `memory` in the [Main WSL Settings](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#main-wsl-settings)

## Getting started

To pull all models, and submodules for tunning the LLM, using

```bash
git clone https://github.com/anhvlt-2k6/osg-ai.git
cd osg-ai 
git submodule update --init --recursive
cd osg-ai && git lfs fetch --all
```

### Prepare `conda` environment

Import and create a new conda environment using this command

```bash
cd ..
conda env create -f .envs/anaconda-env-linux.yaml
```

Then wait until the environment is ready. Once it's done, running

```bash
conda activate osg-ai
```

After that, prepare `docling` of the `conda` environment

```bash
docling-tools models download
```

### Prepare the tunning environment

#### Test GPU

To avoid using CPU from tunning the LLM, run

```bash
cd prepare-env
python3 test_gpu.py
```

If it shows something like...

```bash
GPU is available: ....
```

...then it is good to see. However, if it shows

```bash
Only CPU is available
```

Then you should stop from doing the next step. In that case, review your Linux distro or WSL instance.

#### Prepare documents for tunning

For converting documents, `docconv.py` helps you to prepare the environment.

To change to the directory where the path contains your documents, change the `ROOT` in the line 39. (Make sure the )

```python
39    ROOT = r"../../FPT_BIT_SE_RES/S2 - OSG202" # <- Change the directory
```

And then run it.

```bash
python3 docconv.py
```

### Tunning the LLM

```bash
cd ../training-parse
python3 train.py
python3 convert.py
```

The output model is in `./osg-ai/osg-ai.gguf`

## License

The repo follows the Apache License
