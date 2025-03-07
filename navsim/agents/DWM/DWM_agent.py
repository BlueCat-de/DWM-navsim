from typing import Any, Dict, List, Optional, Union

import pytorch_lightning as pl
import torch
from nuplan.planning.simulation.trajectory.trajectory_sampling import TrajectorySampling
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler

from navsim.agents.abstract_agent import AbstractAgent
from navsim.agents.DWM.DWM_callback import DWMCallback
from navsim.agents.DWM.DWM_config import DWMConfig
from navsim.agents.DWM.DWM_features import (
    DWMFeatureBuilder,
    DWMTargetBuilder,
    DWMMDPBuilder
)
from navsim.agents.DWM.DWM_loss import DWM_loss
from navsim.agents.DWM.DWM_model import DWMModel
from navsim.common.dataclasses import SensorConfig
from navsim.planning.training.abstract_feature_target_builder import (
    AbstractFeatureBuilder,
    AbstractTargetBuilder,
    AbstractMDPBuilder
)


class DWMAgent(AbstractAgent):
    """Agent interface for TransFuser baseline."""

    def __init__(
        self,
        config: DWMConfig,
        lr: float,
        checkpoint_path: Optional[str] = None,
        trajectory_sampling: TrajectorySampling = TrajectorySampling(
            time_horizon=4, interval_length=0.5
        ),
    ):
        """
        Initializes TransFuser agent.
        :param config: global config of TransFuser agent
        :param lr: learning rate during training
        :param checkpoint_path: optional path string to checkpoint, defaults to None
        :param trajectory_sampling: trajectory sampling specification
        """
        super().__init__(trajectory_sampling)

        self._config = config
        self._lr = lr

        self._checkpoint_path = checkpoint_path
        self._DWM_model = DWMModel(self._trajectory_sampling, config)

    def name(self) -> str:
        """Inherited, see superclass."""
        return self.__class__.__name__

    def initialize(self) -> None:
        """Inherited, see superclass."""
        if torch.cuda.is_available():
            state_dict: Dict[str, Any] = torch.load(self._checkpoint_path)["state_dict"]
        else:
            state_dict: Dict[str, Any] = torch.load(
                self._checkpoint_path, map_location=torch.device("cpu")
            )["state_dict"]
        self.load_state_dict(
            {k.replace("agent.", ""): v for k, v in state_dict.items()}
        )

    def get_sensor_config(self) -> SensorConfig:
        """Inherited, see superclass."""
        use_lidar = not self._config.latent
        return SensorConfig.build_all_sensors()

    def get_target_builders(self) -> List[AbstractTargetBuilder]:
        """Inherited, see superclass."""
        return [
            DWMTargetBuilder(
                trajectory_sampling=self._trajectory_sampling, config=self._config
            )
        ]

    def get_feature_builders(self) -> List[AbstractFeatureBuilder]:
        """Inherited, see superclass."""
        return [DWMFeatureBuilder(config=self._config)]

    def get_MDP_builders(self) -> List[AbstractMDPBuilder]:
        return [DWMMDPBuilder(config=self._config)]

    def forward(self, features: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """Inherited, see superclass."""
        return self._DWM_model(features)

    def compute_loss(
        self,
        features: Dict[str, torch.Tensor],
        targets: Dict[str, torch.Tensor],
        predictions: Dict[str, torch.Tensor],
    ) -> torch.Tensor:
        """Inherited, see superclass."""
        return DWM_loss(targets, predictions, self._config)

    def get_optimizers(
        self,
    ) -> Union[Optimizer, Dict[str, Union[Optimizer, LRScheduler]]]:
        """Inherited, see superclass."""
        return torch.optim.Adam(self._DWM_model.parameters(), lr=self._lr)

    def get_training_callbacks(self) -> List[pl.Callback]:
        """Inherited, see superclass."""
        return [DWMCallback(self._config)]
