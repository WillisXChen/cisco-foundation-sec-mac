import strawberry
import typing
import asyncio

# Global storage for the latest stats to avoid circular imports with main.py
# This will be updated by the monitor loop in main.py
_latest_hw_stats_ref = {
    "e_cpu_pct": 0.0, "p_cpu_pct": 0.0, "gpu_pct": 0, "ram_pct": 0.0,
    "ram_used_gb": 0.0, "ram_total_gb": 0.0, "e_cores": 0, "p_cores": 0,
    "gpu_cores": "N/A", "cpu_power_w": 0.0, "gpu_power_w": 0.0,
    "total_power_w": 0.0, "chip_label": "Unknown"
}

@strawberry.type
class HWStats:
    e_cpu_pct: float
    p_cpu_pct: float
    gpu_pct: int
    ram_pct: float
    ram_used_gb: float
    ram_total_gb: float
    e_cores: int
    p_cores: int
    gpu_cores: str
    cpu_power_w: float
    gpu_power_w: float
    total_power_w: float
    chip_label: str

@strawberry.type
class Query:
    @strawberry.field
    def current_stats(self) -> HWStats:
        return HWStats(**_latest_hw_stats_ref)

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def watch_stats(self) -> typing.AsyncGenerator[HWStats, None]:
        while True:
            yield HWStats(**_latest_hw_stats_ref)
            await asyncio.sleep(2)

schema = strawberry.Schema(query=Query, subscription=Subscription)
