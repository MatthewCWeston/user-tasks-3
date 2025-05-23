import numpy as np
from smooth_transition import smooth_transition, SCATTER, BAR, LINE

np.random.seed(123)
N = 15
fd = np.column_stack((np.linspace(0, 10, N), np.random.rand(N) * 10))
td = np.column_stack((np.linspace(0, 10, N), np.random.rand(N) * 10))

# For SCATTER: interpolate both color and size (point size)
ani1 = smooth_transition(
    fd, td, duration=2.0, fps=30, mode=SCATTER,
    from_color='blue', to_color='red',
    from_size=40, to_size=200
)

# For BAR: interpolate both color and width
ani2 = smooth_transition(
    fd, td, duration=2.0, fps=30, mode=BAR,
    from_color='blue', to_color='red',
    from_size=0.1, to_size=.5
)

# For LINE: color interpolation only (no size/linewidth interpolation in current version)
ani3 = smooth_transition(
    fd, td, duration=2.0, fps=30, mode=LINE,
    from_color='blue', to_color='red',
    linewidth=2
)
