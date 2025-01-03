import torch
import ultralytics

# setting device on GPU if available, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
print()

#Additional Info when using cuda
if device.type == 'cuda':
    print(torch.cuda.get_device_name(0))
    print('Memory Usage:')
    print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
    print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')
    print()
    print(f"There are {torch.cuda.device_count()} GPU(s)")
    print(f"current device GPU[{torch.cuda.current_device()}]")

print("===")
print(f"ultralytics version: {ultralytics.__version__}")
