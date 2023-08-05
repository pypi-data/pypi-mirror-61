"""Tests for the ptvpy.process module."""


import pytest
import pandas as pd
import numpy as np
from numpy.testing import assert_allclose

from ptvpy import process
from ptvpy.generate import describe_lines


class Test_particle_velocity:
    @staticmethod
    def _data(x_vel=1, y_vel=2) -> "pd.DataFrame":
        """Create testing data (helper function)."""
        particles = describe_lines(
            frame_count=20,
            particle_count=10,
            x_max=100,
            y_max=100,
            x_vel=x_vel,
            y_vel=y_vel,
            wrap=False,  # Avoid jumps in dx, dy
            seed=42,
        )
        return particles

    def test_copy(self):
        """Check that input dataframe is not modified."""
        df_in = self._data()
        df_out = process.particle_velocity(df_in)
        assert df_in is not df_out

    @pytest.mark.parametrize("step", [1, 5, 10, np.int(1)])
    def test_empty_data(self, step):
        """Check behavior for an empty DataFrame."""
        empty_data = self._data().iloc[:0, :]
        assert empty_data.shape == (0, 4)
        result = process.particle_velocity(empty_data, step=step)
        assert result.shape == (0, 7)

    @pytest.mark.parametrize("step", [1, 5, 10, np.int(1)])
    def test_const_velocity(self, step):
        """Check behavior for particles with constant velocity."""
        x_vel, y_vel = 1, 2
        result = process.particle_velocity(self._data(x_vel, y_vel), step=step)
        # Step size should have no effect with constant velocity
        assert_allclose(result["dx"].dropna(), x_vel)
        assert_allclose(result["dy"].dropna(), y_vel)
        assert_allclose(result["v"].dropna(), np.linalg.norm([x_vel, y_vel]))
        particle_no = result["particle"].nunique()
        # Number on nans should be step * particle_no, because averaging only
        # works after skipping the first `step` rows
        not_nan_count = len(result) - step * particle_no
        assert len(result["dx"].dropna()) == not_nan_count
        assert len(result["dy"].dropna()) == not_nan_count
        assert len(result["v"].dropna()) == not_nan_count

    @pytest.mark.parametrize("step", [1, 5, 10, np.int(1)])
    def test_third_dimension(self, step):
        """Check behavior for particles with constant velocity."""
        x_vel, y_vel = 1, 2
        particles = self._data(x_vel, y_vel)
        particles["z"] = particles["x"] + particles["y"]

        result = process.particle_velocity(particles, step=step)
        # Step size should have no effect with constant velocity
        assert_allclose(result["dx"].dropna(), x_vel)
        assert_allclose(result["dy"].dropna(), y_vel)
        assert_allclose(result["dz"].dropna(), x_vel + y_vel)
        assert_allclose(
            result["v"].dropna(), np.linalg.norm([x_vel, y_vel, x_vel + y_vel])
        )
        particle_no = result["particle"].nunique()
        # Number on nans should be step * particle_no, because averaging only
        # works after skipping the first `step` rows
        not_nan_count = len(result) - step * particle_no
        assert len(result["dx"].dropna()) == not_nan_count
        assert len(result["dy"].dropna()) == not_nan_count
        assert len(result["dz"].dropna()) == not_nan_count
        assert len(result["v"].dropna()) == not_nan_count

    @pytest.mark.parametrize("step", [-1, 0, np.iinfo(np.int64).min])
    def test_step_value_error(self, step):
        with pytest.raises(ValueError, match="step must be at least 1, was"):
            process.particle_velocity(self._data(), step=step)


def test_find_helix_particles():
    """Simple test that compares results with reviewed DataFrames."""
    points = pd.DataFrame([(0, 0), (1, 1), (0, 2), (2, 1)], columns=("x", "y"))

    pairs = process.find_helix_particles(
        points, 1, np.sqrt(5), unique=False, save_old_pos=True
    )

    # Guard against naming the third dimension anything but "z" ensuring that it is
    # automatically picked up by trackpy as a coordinate during linking
    assert "z" in pairs.columns

    desired = {
        "x": [0.5, 0.0, 1.0, 0.5, 1.5, 1.0],
        "y": [0.5, 1.0, 0.5, 1.5, 1.0, 1.5],
        "x_old_1": [0, 0, 0, 1, 1, 0],
        "x_old_2": [1, 0, 2, 0, 2, 2],
        "y_old_1": [0, 0, 0, 1, 1, 2],
        "y_old_2": [1, 2, 1, 2, 1, 1],
        "z": [np.pi / 4, np.pi / 2, np.arctan(0.5), -np.pi / 4, 0, -np.arctan(0.5)],
        "pair_distance": [np.sqrt(2), 2, np.sqrt(5), np.sqrt(2), 1, np.sqrt(5)],
    }
    pd.testing.assert_frame_equal(pairs, pd.DataFrame(desired))

    # Demanding that each particle only appears once should return two pairs
    pairs = process.find_helix_particles(points, 0, 100, unique=True)
    desired = {
        "x": [1.5, 0.0],
        "y": [1.0, 1.0],
        "z": [0.0, np.pi / 2],
        "pair_distance": [1.0, 2.0],
    }
    pd.testing.assert_frame_equal(pairs, pd.DataFrame(desired))

    # Increasing the minimum distance should force different pairs
    pairs = process.find_helix_particles(points, np.sqrt(2), 100, unique=True)
    desired = {
        "x": [0.5, 1.0],
        "y": [0.5, 1.5],
        "z": [np.pi / 4, -np.arctan(0.5)],
        "pair_distance": [np.sqrt(2), np.sqrt(5)],
    }
    pd.testing.assert_frame_equal(pairs, pd.DataFrame(desired))
