import torch

if torch.cuda.is_available():
    print("GPU is available:", torch.cuda.get_device_name(), sep="\t")
else:
    print("Only CPU is available")