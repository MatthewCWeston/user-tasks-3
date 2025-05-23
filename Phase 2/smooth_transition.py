import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Chart type constants
SCATTER = "scatter"
BAR = "bar"
LINE = "line"

def to_rgba_array(color, N):
    """Convert color to an (N, 4) array of RGBA floats."""
    import matplotlib.colors as mcolors
    if isinstance(color, str) or (isinstance(color, tuple) and len(color) in (3, 4)):
        return np.tile(mcolors.to_rgba(color), (N, 1))
    arr = np.array(color)
    if arr.ndim == 1:
        return np.tile(mcolors.to_rgba(arr), (N, 1))
    if arr.shape[0] == N:
        if arr.shape[1] == 3:
            alpha = np.ones((N, 1))
            arr = np.concatenate([arr, alpha], axis=1)
        return arr
    raise ValueError("from_color and to_color must be broadcastable to (N, 4)")

def to_size_array(size, N, default=40):
    """Convert size to an (N,) array of floats."""
    if size is None:
        return np.full((N,), default)
    arr = np.array(size)
    if arr.size == 1:
        return np.full((N,), arr.item())
    if arr.shape == (N,):
        return arr
    raise ValueError("from_size and to_size must be broadcastable to (N,)")

def smooth_transition(from_data, to_data, duration=1.0, fps=30, **kwargs):
    """
    Animates a smooth transition between two sets of (N, 2) datapoints,
    optionally including color and size interpolation.
    
    Args:
        from_data (np.ndarray): Starting data, shape (N, 2)
        to_data (np.ndarray): Ending data, shape (N, 2)
        duration (float): Duration in seconds
        fps (int): Frames per second
        mode (str): One of "scatter", "bar", or "line"
        from_color: Starting color(s) (matplotlib color or (N, 3)/(N, 4) array)
        to_color: Ending color(s) (matplotlib color or (N, 3)/(N, 4) array)
        from_size: Starting sizes (scalar or (N,) array)
        to_size: Ending sizes (scalar or (N,) array)
        **kwargs: Additional keyword arguments passed to matplotlib functions
    """
    assert from_data.shape == to_data.shape, "from_data and to_data must have the same shape"
    assert from_data.shape[1] == 2, "Data must be of shape (N, 2)"
    mode = kwargs.get("mode", SCATTER)
    n_frames = int(duration * fps)
    # Handle color interpolation
    from_color = kwargs.pop("from_color", None)
    to_color = kwargs.pop("to_color", None)
    color_interp = from_color is not None and to_color is not None
    # Handle size interpolation
    from_size = kwargs.pop("from_size", None)
    to_size = kwargs.pop("to_size", None)
    size_interp = from_size is not None and to_size is not None
    N = from_data.shape[0]
    if color_interp:
        from_color_arr = to_rgba_array(from_color, N)
        to_color_arr = to_rgba_array(to_color, N)
    if size_interp:
        from_size_arr = to_size_array(from_size, N)
        to_size_arr = to_size_array(to_size, N)
    fig, ax = plt.subplots()
    # Prepare plot objects for each mode
    plot_kwargs = {k: v for k, v in kwargs.items() if k not in ["mode", "from_color", "to_color", "from_size", "to_size"]}
    if mode == SCATTER:
        scatter_color = from_color_arr if color_interp else plot_kwargs.pop("c", None)
        scatter_size = from_size_arr if size_interp else plot_kwargs.pop("s", None)
        plot_obj = ax.scatter(from_data[:, 0], from_data[:, 1], c=scatter_color, s=scatter_size, **plot_kwargs)
    elif mode == BAR:
        width = from_size_arr if size_interp else plot_kwargs.pop("width", 0.8)
        # If width is scalar, make it array
        if isinstance(width, (int, float)):
            width_arr = np.full((N,), width)
        else:
            width_arr = np.array(width)
        bar_color = from_color_arr if color_interp else plot_kwargs.pop("color", None)
        plot_obj = ax.bar(from_data[:, 0], from_data[:, 1], width=width_arr, color=bar_color, **plot_kwargs)
    elif mode == LINE:
        line_color = from_color_arr[0] if color_interp else plot_kwargs.pop("color", None)
        plot_obj, = ax.plot(from_data[:, 0], from_data[:, 1], color=line_color, **plot_kwargs)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    # Set reasonable axis limits
    all_x = np.concatenate([from_data[:, 0], to_data[:, 0]])
    all_y = np.concatenate([from_data[:, 1], to_data[:, 1]])
    pad_x = (all_x.max() - all_x.min()) * 0.05 or 1
    pad_y = (all_y.max() - all_y.min()) * 0.08 or 1
    ax.set_xlim(all_x.min() - pad_x, all_x.max() + pad_x)
    ax.set_ylim(all_y.min() - pad_y, all_y.max() + pad_y)
    ax.set_title(f"Smooth transition: {mode}")
    # Tweening function (linear interpolation)
    def interpolate(start, end, t):
        return start + (end - start) * t
    def update(frame):
        t = frame / n_frames
        cur_data = interpolate(from_data, to_data, t)
        if color_interp:
            cur_color = interpolate(from_color_arr, to_color_arr, t)
        if size_interp:
            cur_size = interpolate(from_size_arr, to_size_arr, t)
        if mode == SCATTER:
            plot_obj.set_offsets(cur_data)
            if color_interp:
                plot_obj.set_facecolor(cur_color)
            if size_interp:
                plot_obj.set_sizes(cur_size)
        elif mode == BAR:
            # width is animated
            if size_interp:
                cur_width = cur_size
            else:
                cur_width = np.array([rect.get_width() for rect in plot_obj])
            for i, (rect, (x, height)) in enumerate(zip(plot_obj, cur_data)):
                rect.set_height(height)
                rect.set_x(x - cur_width[i] / 2)
                rect.set_width(cur_width[i])
                if color_interp:
                    rect.set_facecolor(cur_color[i])
        elif mode == LINE:
            plot_obj.set_data(cur_data[:, 0], cur_data[:, 1])
            if color_interp:
                plot_obj.set_color(cur_color[0])
        return plot_obj,
    ani = FuncAnimation(fig, update, frames=n_frames + 1, interval=1000 / fps, blit=False)
    plt.show()
    return ani  # Return the animation object for further handling
