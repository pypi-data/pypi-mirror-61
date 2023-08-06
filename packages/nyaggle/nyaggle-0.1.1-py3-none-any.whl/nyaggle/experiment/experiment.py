import json
import os
import shutil
import uuid
import warnings
from logging import getLogger, FileHandler, DEBUG, Logger
from typing import Dict, Optional

import numpy as np
import pandas as pd

from nyaggle.environment import requires_mlflow

MLFLOW_KEY_LENGTH_LIMIT = 250
MLFLOW_VALUE_LENGTH_LIMIT = 250


def _sanitize_mlflow_param(param, limit):
    if len(str(param)) > limit:
        warnings.warn('Length of param exceeds limit {}. It will be truncated. value: {}'.format(limit, param))
        param = str(param)[:limit]
    return param


class Experiment(object):
    """Minimal experiment logger for Kaggle

    This module provides minimal functionality for logging Kaggle experiments.
    The output files are laid out as follows:

    .. code-block:: none

      <logging_directory>/
          <log_filename>            <== output of log()
          <metrics_filename>        <== output of log_metrics(), format: name,score
          <params_filename>         <== output of log_param(), format: key,value
          mlflow.json               <== (optional) corresponding mlflow's run_id, experiment_id are logged.


    You can add numpy array and pandas dataframe under the directory through ``log_numpy`` and ``log_dataframe``.

    Args:
        logging_directory:
            Path to directory where output is stored.
        overwrite:
            If True, contents in ``logging_directory`` will be overwritten.
        custom_logger:
            A custom logger to be used instead of default logger.
        with_mlflow:
            If True, `mlflow tracking <https://www.mlflow.org/docs/latest/tracking.html>`_ is used.
            One instance of ``nyaggle.experiment.Experiment`` corresponds to one run in mlflow.
            Note that all output files are located both ``logging_directory`` and
            mlflow's directory (``mlruns`` by default).
    """

    def __init__(self,
                 logging_directory: str,
                 overwrite: bool = False,
                 custom_logger: Optional[Logger] = None,
                 with_mlflow: bool = False,
                 mlflow_run_id: Optional[str] = None,
                 logging_mode: str = 'w'
                 ):
        os.makedirs(logging_directory, exist_ok=overwrite)
        self.logging_directory = logging_directory
        self.with_mlflow = with_mlflow

        if custom_logger is not None:
            self.logger = custom_logger
            self.is_custom = True
        else:
            self.logger = getLogger(str(uuid.uuid4()))
            self.log_path = os.path.join(logging_directory, 'log.txt')
            self.logger.addHandler(FileHandler(self.log_path))
            self.logger.setLevel(DEBUG)
            self.is_custom = False
        self.metrics_path = os.path.join(logging_directory, 'metrics.txt')
        self.metrics = open(self.metrics_path, mode=logging_mode)
        self.params = open(os.path.join(logging_directory, 'params.txt'), mode=logging_mode)
        self.inherit_existing_run = False

        if self.with_mlflow:
            requires_mlflow()
            self.mlflow_run_id = mlflow_run_id
            if mlflow_run_id is not None:
                self.mlflow_run_name = None
            else:
                self.mlflow_run_name = logging_directory

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.stop()

    @classmethod
    def continue_from(cls, logging_directory: str):
        params = {
            'logging_directory': logging_directory,
            'overwrite': True,
            'logging_mode': 'a'
        }

        mlflow_path = os.path.join(logging_directory, 'mlflow.json')
        if os.path.exists(mlflow_path):
            with open(mlflow_path, 'r') as f:
                mlflow_metadata = json.load(f)

                params['with_mlflow'] = True
                params['mlflow_run_id'] = mlflow_metadata['run_id']

        return cls(**params)

    def start(self):
        """
        Start a new experiment.
        """
        if self.with_mlflow:
            import mlflow

            if mlflow.active_run() is not None:
                active_run = mlflow.active_run()
                self.inherit_existing_run = True
            else:
                active_run = mlflow.start_run(run_name=self.mlflow_run_name, run_id=self.mlflow_run_id)
            mlflow_metadata = {
                'artifact_uri': active_run.info.artifact_uri,
                'experiment_id': active_run.info.experiment_id,
                'run_id': active_run.info.run_id
            }
            with open(os.path.join(self.logging_directory, 'mlflow.json'), 'w') as f:
                json.dump(mlflow_metadata, f, indent=4)

    def stop(self):
        """
        Stop current experiment.
        """
        self.metrics.close()
        self.params.close()

        if not self.is_custom:
            for h in self.logger.handlers:
                h.close()

        if self.with_mlflow:
            import mlflow
            mlflow.log_artifact(self.log_path)
            mlflow.log_artifact(self.metrics_path)
            if not self.inherit_existing_run:
                mlflow.end_run()

    def get_logger(self) -> Logger:
        """
        Get logger used in this experiment.

        Returns:
            logger object
        """
        return self.logger

    def get_run(self):
        """
        Get mlflow's currently active run, or None if ``with_mlflow = False``.

        Returns:
            active Run
        """
        if not self.with_mlflow:
            return None

        import mlflow
        return mlflow.active_run()

    def log(self, text: str):
        """
        Logs a message on the logger for the experiment.

        Args:
            text:
                The message to be written.
        """
        self.logger.info(text)

    def log_param(self, key, value):
        """
        Logs a key-value pair for the experiment.

        Args:
            key: parameter name
            value: parameter value
        """
        self.params.write('{},{}\n'.format(key, value))
        self.params.flush()

        if self.with_mlflow:
            import mlflow
            key_mlflow = _sanitize_mlflow_param(key, MLFLOW_KEY_LENGTH_LIMIT)
            value_mlflow = _sanitize_mlflow_param(value, MLFLOW_VALUE_LENGTH_LIMIT)
            mlflow.log_param(key_mlflow, value_mlflow)

    def log_params(self, params: Dict):
        """
        Logs a batch of params for the experiments.

        Args:
            params: dictionary of parameters
        """
        for k, v in params.items():
            self.log_param(k, v)

    def log_metric(self, name: str, score: float):
        """
        Log a metric under the logging directory.

        Args:
            name:
                Metric name.
            score:
                Metric value.
        """
        self.metrics.write('{},{}\n'.format(name, score))
        self.metrics.flush()

        if self.with_mlflow:
            import mlflow
            mlflow.log_metric(name, score)

    def log_numpy(self, name: str, array: np.ndarray):
        """
        Log a numpy ndarray under the logging directory.

        Args:
            name:
                Name of the file. A .npy extension will be appended to the file name if it does not already have one.
            array:
                Array data to be saved.
        """
        path = os.path.join(self.logging_directory, name)
        np.save(path, array)

        if self.with_mlflow:
            import mlflow
            mlflow.log_artifact(path + '.npy')

    def log_dataframe(self, name: str, df: pd.DataFrame, file_format: str = 'feather'):
        """
        Log a pandas dataframe under the logging directory.

        Args:
            name:
                Name of the file. A ``.f`` or ``.csv`` extension will be appended to the file name
                if it does not already have one.
            df:
                A dataframe to be saved.
            file_format:
                A format of output file. ``csv`` and ``feather`` are supported.
        """
        path = os.path.join(self.logging_directory, name)
        if file_format == 'feather':
            if not path.endswith('.f'):
                path += '.f'
            df.to_feather(path)
        elif file_format == 'csv':
            if not path.endswith('.csv'):
                path += '.csv'
            df.to_csv(path, index=False)
        else:
            raise RuntimeError('format not supported')

        if self.with_mlflow:
            import mlflow
            mlflow.log_artifact(path)

    def log_artifact(self, src_file_path: str):
        """
        Make a copy of the file under the logging directory.

        Args:
            src_file_path:
                Path of the file. If path is not a child of the logging directory, the file will be copied.
                If ``with_mlflow`` is True, ``mlflow.log_artifact`` will be called (then another copy will be made).
        """
        logging_path = os.path.abspath(self.logging_directory)
        src_file_path = os.path.abspath(src_file_path)

        if os.path.commonpath([logging_path]) != os.path.commonpath([logging_path, src_file_path]):
            src_file = os.path.basename(src_file_path)
            shutil.copy(src_file, self.logging_directory)

        if self.with_mlflow:
            import mlflow
            mlflow.log_artifact(src_file_path)


def add_leaderboard_score(logging_directory: str, score: float):
    """
    Record leaderboard score to the existing experiment directory.

    Args:
        logging_directory:
            The directory to be added
        score:
            Leaderboard score
    """
    with Experiment.continue_from(logging_directory) as e:
        e.log_metric('LB', score)