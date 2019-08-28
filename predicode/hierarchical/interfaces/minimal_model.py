"""Interface to the minimal model, linear predictive coding with a single hidden
layer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import tensorflow as tf
import keras
import numpy as np
import tqdm

from predicode.hierarchical.initializer import weight_init, init

def hierarchical_config(initializer='random')

class MinimalHierarchicalModel(): # pylint:disable=too-many-instance-attributes
    """Interface to the minimal hierarchical model.

    The minimal hierarchical model is given by a linear predictive coding model
    with one densely connected, linear layer.

    Args:
        input_data: A numpy array, where the columns correspond to the
            dimensions and the rows correspond to the number of observations.
        input_dimensions: Input dimensions.
        n_observations: Number of observations.
        latent_dimensions: Dimensions of the latent layer.
        weights: An object that can be fed through
            :fun:`~predicode.weight_init`.
        use_bias: Should the model use an additional bias layer?"""
    parameter_classes = []
    @classmethod
    def parameter_classes(cls, )

    @staticmethod
    def _state_estimator_predict(mode, flipped_graph):
        return flipped_graph

    @staticmethod
    def _state_estimator_loss(flipped_graph, labels):
        loss = tf.losses.mean_squared_error(flipped_graph, labels)
        return loss

    def _state_estimator_train(self, mode, flipped_graph, labels,
                               learning_rate=1):
        loss = self._state_estimator_loss(flipped_graph, labels)
        optimizer = keras.train.GradientDescentOptimizer(
            learning_rate=learning_rate
        )
        train_op = optimizer.minimize(
            loss, global_step=tf.train.get_global_step()
        )
        return (loss, train_op)

    def _estimator(self, latent_values, observed, weights):
        _input = tf.Variable(latent_values)
        _weights = tf.constant(weights.T)
        _observed = tf.constant(observed)
        prediction = tf.matmul(_input, _weights)
        loss = tf.losses.mean_squared_error(prediction, _observed)
        optimizer = tf.train.GradientDescentOptimizer(
            learning_rate=learning_rate
        )

    def __init__(self, input_data,
                 weight_config=HierarchicalConfig(
                     initializer='random',
                     optimizer=tf.train.GradientDescentOptimizer(
                         learning_rate=1
                     ),
                     epsilon=1e-3
                 ),
                 state_config=HierarchicalConfig(
                     initializer='random',
                     optimizer=tf.train.GradientDescentOptimizer(
                         learning_rate=1
                     ),
                     epsilon=1e-3
                 )):
        self.input_data = input_data
        self.input_dimensions = input_data.shape[1]
        self.n_observations = input_data.shape[0]
        self.latent_dimensions = latent_dimensions
        self._weight_config = weight_config
        self._state_config = state_config

        self.initialize_parameters()
        
        

        self._weights = weight_init(weights,
                                    input_data=input_data,
                                    latent_dimensions=latent_dimensions,
                                    input_dimensions=self.input_dimensions)
        self._latent_values = weight_init('random',
                                          input_dimensions=self.n_observations,
                                          latent_dimensions=latent_dimensions)

        assert self.input_dimensions == self._weights.shape[0]
        assert self.latent_dimensions == self._weights.shape[1]

        kwargs['use_bias'] = use_bias
        kwargs['n_observations'] = self.n_observations
        kwargs['latent_weights'] = [
            tf.feature_column.numeric_column(
                key=key, dtype=tf.float64
            ) for key in self._dct_weights.keys()
        ]
        kwargs['state_learning_rate'] = state_learning_rate

        self._kwargs = kwargs

        self._state = tf.estimator.Estimator(
            model_fn=self._state_estimator,
            params=kwargs
        )
        self._state.config.replace(save_summary_steps=10)

        self.activate('state', 'simulation')

    def initialize_parameters(self, initializer=None, range='activated'):
        """Initialize state and weight parameters.

        Initialize the parameters either according to their configuration or
        according to a specified initializer.
        
        Args:
            initializer: If None (default value), use the specified initializer.
                Otherwise, specify an initializer that can be assigned by the
                given configuration.
            range: If you would like to specify your own range, set this range
                to a list of possible values. Default is the special"""

    @staticmethod
    def _validate_estimation(what):
        if what not in ['state', 'weight']:
            raise ValueError(
                'You must either activate "state" or "weight" estimation.'
            )
        return what

    @staticmethod
    def _validate_method(what):
        if what not in ['simulation', 'analytical']:
            raise ValueError(
                'You must either activate "simulation" or "analytical" method.'
            )
        return what

    def activate(self, estimation=None, method=None):
        """Activate state or weight estimation and method to solve the model.

        Args:
            estimation: 'state' or 'weight'.
            method: 'simulated' or analytical'."""
        if estimation:
            estimation = self._validate_estimation(estimation)
            self._estimation = estimation
        if method:
            method = self._validate_method(method)
            self._method = method

    @property
    def estimation(self):
        """Are states or weights currently estimated?"""
        return self._estimation

    @property
    def method(self):
        """Is the model computing simulated or analytical solutions?"""
        return self._method

    def activate_state_estimation(self):
        """Activate state estimation."""
        self.activate(estimation='state')

    def activate_weight_estimation(self):
        """Activate weight estimation."""
        self.activate(estimation='weight')

    def activate_simulated_method(self):
        """Activate simulated method."""
        self.activate(method='simulated')

    def activate_analytical_method(self):
        """Activate analytical method."""
        self.activate(method='analytical')

    def train(self, steps=None, max_steps=None, learning_rate=None, **kwargs):
        """Train the network.

        Args:
            steps: Number of steps (see Tensorflow documentation).
            max_steps: Number of steps.
            learning_rate: Learning rate (see Tensorflow documentation).
            kwargs: Additional arguments."""
        if self.estimation == 'state':
            if learning_rate is not None:
                if learning_rate != self._kwargs['state_learning_rate']:
                    self._kwargs['state_learning_rate'] = learning_rate
                    self._state = tf.estimator.Estimator(
                        model_fn=self._state_estimator,
                        params=self._kwargs
                    )

            return self._state.train(
                input_fn=lambda: (self._dct_weights, self.input_data.T),
                steps=steps,
                max_steps=max_steps,
                **kwargs
            )
        raise NotImplementedError()

    def evaluate(self, **kwargs):
        """Evaluate network.

        Args:
            kwargs: Additional parameters for tf.Estimator.evaluate().

        Returns:
            Statistics of the trained model."""
        if self.estimation == 'state':
            return self._state.evaluate(
                input_fn=lambda: (self._dct_weights, self.input_data.T),
                steps=1,
                **kwargs
            )
        raise NotImplementedError()

    def predict(self, **kwargs):
        """Predict the input data according to the model.

        Args:
            kwargs: Additional parameters for tf.Estimator.predict().

        Returns:
            Prediction as a two-dimensional numpy array with the same form as
            the input data."""
        if self.estimation == 'state':
            generator = self._state.predict(
                input_fn=lambda: (self._dct_weights, self.input_data.T),
                **kwargs)
            prediction_lst = [
                next(generator) for i in range(self.input_dimensions)
            ]
            prediction = np.array(prediction_lst).T
            return prediction
        raise NotImplementedError()

    def learning_curve(self, steps=1e4, resolution=1, learning_rate=None,
                       **kwargs):
        """Get the learning curve.

        Args:
            steps: For how many steps would you like the learning curve?
            resolution: In what resolution (in steps) would you like to
                determine the learning curve?
            learning_rate: You can optionally specify a learning rate.
            kwargs: Other arguments.

        Returns:
            Three dimensional numpy array: observations x latent dimensions x
            steps."""
        tsteps = math.ceil(steps/resolution)
        steps_per_tstep = steps/tsteps
        _learning_curve = np.empty(dtype=np.float64,
                                   shape=(self.n_observations,
                                          self.latent_dimensions,
                                          tsteps))
        prev_verbosity = tf.logging.get_verbosity()
        tf.logging.set_verbosity(tf.logging.ERROR)
        for i in tqdm.trange(tsteps):
            self.train(steps=steps_per_tstep, learning_rate=learning_rate,
                       **kwargs)
            _learning_curve[:, :, i] = self.latent_values
        tf.logging.set_verbosity(prev_verbosity)
        return _learning_curve

    @property
    def latent_values(self):
        """Get the latent values.

        Returns:
            The latent variables for the input data as a two-dimensional numpy
            array. Each observation is one row and each latent dimension one
            column."""
        return self._state.get_variable_value('dense/kernel').T

    @property
    def weights(self):
        """Get the weights.

        Returns:
            The weights of the minimal model with the rotation that returns one
            input dimension per row."""
        return self._weights
