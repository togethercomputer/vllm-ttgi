import enum
from platform import uname
import uuid

import psutil
import torch

import vllm_cuda_utils


class Device(enum.Enum):
    GPU = enum.auto()
    CPU = enum.auto()


def get_max_shared_memory_bytes(gpu: int = 0) -> int:
    """Returns the maximum shared memory per thread block in bytes."""
    # https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__TYPES.html
    cudaDevAttrMaxSharedMemoryPerBlockOptin = 97  # pylint: disable=invalid-name
    max_shared_mem = vllm_cuda_utils.get_device_attribute(
        cudaDevAttrMaxSharedMemoryPerBlockOptin, gpu)
    return int(max_shared_mem)


class Counter:

    def __init__(self, start: int = 0) -> None:
        self.counter = start

    def __next__(self) -> int:
        id = self.counter
        self.counter += 1
        return id

    def reset(self) -> None:
        self.counter = 0


def get_gpu_memory(gpu: int = 0) -> int:
    """Returns the total memory of the GPU in bytes."""
    return torch.cuda.get_device_properties(gpu).total_memory


def get_cpu_memory() -> int:
    """Returns the total CPU memory of the node in bytes."""
    return psutil.virtual_memory().total


def random_uuid() -> str:
    return str(uuid.uuid4().hex)

def in_wsl() -> bool:
    # Reference: https://github.com/microsoft/WSL/issues/4071
    return "microsoft" in " ".join(uname()).lower()
