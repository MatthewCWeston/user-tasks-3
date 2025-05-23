import numpy as np
from matplotlib.smooth_transition import smooth_transition, SCATTER, BAR, LINE

np.random.seed(123)
N = 15
fd = np.column_stack((np.linspace(0, 10, N), np.random.rand(N) * 10))
td = np.column_stack((np.linspace(0, 10, N), np.random.rand(N) * 10))

ani1 = smooth_transition(
    fd, td, duration=2.0, fps=30, mode=SCATTER,
    from_color='blue', to_color='red',
    from_size=40, to_size=200,
    easing='linear',
    title="Scatterplot"
)

ani2 = smooth_transition(
    fd, td, duration=2.0, fps=30, mode=BAR,
    from_color='blue', to_color='red',
    from_size=0.1, to_size=.5,
    easing='ease-in',
    title="Bar Graph"
)

ani3 = smooth_transition(
    fd, td, duration=2.0, fps=30, mode=LINE,
    from_color='blue', to_color='red',
    linewidth=2,
    easing='ease-out',
    title="Line Graph"
)

# Save animations as GIFs (fps already specified in animation, no need to repeat)
ani1.save('scatter_transition.gif', writer='pillow')
ani2.save('bar_transition.gif', writer='pillow')
ani3.save('line_transition.gif', writer='pillow')
