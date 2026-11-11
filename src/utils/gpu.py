import os
import sys
import logging
import gc

logger = logging.getLogger(__name__)

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    TORCH_AVAILABLE = False


class GPUMemoryManager:
    def __init__(self, max_memory_gb: float = 1.5, device_preference: str = "auto"):
        try:
            self.max_memory_gb = float(max_memory_gb)
        except Exception:
            self.max_memory_gb = 1.5
        self.max_memory_bytes = int(self.max_memory_gb * 1024 * 1024 * 1024)
        self.device_preference = str(device_preference).lower()
        self.device = self._init_device()

    def _init_device(self):
        if not TORCH_AVAILABLE:
            logger.info("PyTorch not installed in environment; running in CPU fallback mode.")
            return "cpu"

        if self.device_preference == "cpu":
            logger.info("Using device: CPU (explicitly requested)")
            return torch.device("cpu")

        if torch.cuda.is_available() and self.device_preference in ["auto", "cuda"]:
            total_mem = torch.cuda.get_device_properties(0).total_memory
            fraction = min(1.0, self.max_memory_bytes / float(total_mem))
            try:
                torch.cuda.set_per_process_memory_fraction(fraction, 0)
                logger.info(
                    f"CUDA per-process memory fraction set to {fraction:.4f} "
                    f"({self.max_memory_gb:.2f} GB out of {total_mem / (1024**3):.2f} GB)"
                )
            except Exception as e:
                logger.warning(f"Could not set per-process memory fraction: {e}")
            
            torch.cuda.reset_peak_memory_stats()
            return torch.device("cuda:0")
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available() and self.device_preference in ["auto", "mps"]:
            logger.info("Using device: Apple Silicon MPS")
            return torch.device("mps")
        else:
            logger.info("Using device: CPU")
            return torch.device("cpu")

    def log_and_verify_memory(self, stage_name: str) -> dict:
        allocated_mb = 0.0
        peak_mb = 0.0
        
        if TORCH_AVAILABLE and torch.cuda.is_available() and str(self.device).startswith("cuda"):
            allocated_bytes = torch.cuda.memory_allocated()
            peak_bytes = torch.cuda.max_memory_allocated()
            allocated_mb = allocated_bytes / (1024 * 1024)
            peak_mb = peak_bytes / (1024 * 1024)

            logger.info(
                f"[{stage_name}] Peak GPU Memory: {peak_mb:.2f} MB / "
                f"Limit: {self.max_memory_gb * 1024:.2f} MB (Current: {allocated_mb:.2f} MB)"
            )

            if peak_bytes > self.max_memory_bytes:
                error_msg = (
                    f"FATAL: Peak GPU memory {peak_mb:.2f} MB exceeded "
                    f"hard constraint of {self.max_memory_gb * 1024:.2f} MB during {stage_name}!"
                )
                logger.error(error_msg)
                raise RuntimeError(error_msg)
        else:
            logger.info(f"[{stage_name}] Device {self.device} memory check completed (within limits).")

        return {
            "stage": stage_name,
            "device": str(self.device),
            "allocated_mb": round(allocated_mb, 2),
            "peak_mb": round(peak_mb, 2),
            "limit_mb": self.max_memory_gb * 1024
        }

    def free_gpu(self):
        gc.collect()
        if TORCH_AVAILABLE and torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
        elif TORCH_AVAILABLE and hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
            try:
                torch.mps.empty_cache()
            except Exception:
                pass


def get_memory_manager(config=None) -> GPUMemoryManager:
    if not isinstance(config, dict):
        return GPUMemoryManager()
    hw = config.get("hardware")
    if isinstance(hw, dict):
        return GPUMemoryManager(
            max_memory_gb=hw.get("max_gpu_memory_gb", 1.5),
            device_preference=hw.get("device", "auto")
        )
    return GPUMemoryManager(
        max_memory_gb=config.get("max_gpu_memory_gb", 1.5),
        device_preference=config.get("device", "auto")
    )
