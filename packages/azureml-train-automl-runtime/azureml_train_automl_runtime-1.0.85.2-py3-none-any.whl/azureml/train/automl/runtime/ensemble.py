# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for creating ensembles from previous automated machine learning iterations."""
from typing import Any, cast, Dict, Union

from azureml.automl.runtime import voting_ensemble_base
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from . import _ensemble_helper


class Ensemble(voting_ensemble_base.VotingEnsembleBase):
    """
    Class for ensembling previous AutoML iterations.

    The ensemble pipeline is initialized from a collection of already fitted pipelines.


    :param automl_settings -- The settings for this current experiment
    :param ensemble_run_id -- The id of the current ensembling run
    :param experiment_name -- The name of the current Azure ML experiment
    :param workspace_name --  The name of the current Azure ML workspace where the experiment is run
    :param subscription_id --  The id of the current Azure ML subscription where the experiment is run
    :param resource_group_name --  The name of the current Azure resource group
    """

    def __init__(self,
                 automl_settings: Union[str, Dict[str, Any], AzureAutoMLSettings],
                 ensemble_run_id: str,
                 experiment_name: str,
                 workspace_name: str,
                 subscription_id: str,
                 resource_group_name: str):
        """Create an Ensemble pipeline out of a collection of already fitted pipelines.

        :param automl_settings -- The settings for this current experiment
        :param ensemble_run_id -- The id of the current ensembling run
        :param experiment_name -- The name of the current Azure ML experiment
        :param workspace_name --  The name of the current Azure ML workspace where the experiment is run
        :param subscription_id --  The id of the current Azure ML subscription where the experiment is run
        :param resource_group_name --  The name of the current Azure resource group
        """
        super(Ensemble, self).__init__(automl_settings, AzureAutoMLSettings)
        self.helper = _ensemble_helper.EnsembleHelper(
            cast(AzureAutoMLSettings, self._automl_settings),
            ensemble_run_id,
            experiment_name,
            workspace_name,
            subscription_id,
            resource_group_name)

    def _download_fitted_models_for_child_runs(self, logger, child_runs, model_remote_path):
        """Override the base implementation for downloading the fitted pipelines in an async manner.

        :param logger -- logger instance
        :param child_runs -- collection of child runs for which we need to download the pipelines
        :param model_remote_path -- the remote path where we're downloading the pipelines from
        """
        return self.helper.download_fitted_models_for_child_runs(logger, child_runs, model_remote_path)

    def _get_ensemble_and_parent_run(self):
        return self.helper.get_ensemble_and_parent_run()

    def _get_logger(self):
        return self.helper.get_logger()


class VotingEnsemble(Ensemble):
    """Class for creating a SoftVoting Ensemble out of previous AutoML iterations."""

    pass
