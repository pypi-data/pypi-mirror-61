# ing-theme-matplotlib

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/pypi/pyversions/qbstyles.svg)](https://pypi.org/project/ing-theme-matplotlib/)
[![PyPI version](https://badge.fury.io/py/ing-theme-matplotlib.svg)](https://pypi.org/project/ing-theme-matplotlib/)
[![downloads](https://img.shields.io/pypi/dm/ing_theme_matplotlib)](https://img.shields.io/pypi/dm/ing_theme_matplotlib)

`ing_theme_matplotlib` is a python package with a light and a dark [`matplotlib`](https://github.com/matplotlib/matplotlib) style that allows you to create your plots using ING colors and ING Me font. It was adapted from the [`qbstyles`](https://github.com/quantumblacklabs/qbstyles) package.

Dark style | Light style
|-----------|----------- |
| ![Scatter plot](https://gitlab.com/ing_rpaa/ing_theme_matplotlib/uploads/e695ba1c207af8045d5117c8cb84690e/scatter_dark.png "Scatter plot") | ![Distribution plot](https://gitlab.com/ing_rpaa/ing_theme_matplotlib/uploads/c649e6457e47ea70e21cf214b02180cb/dist_light.png "Distribution plot") |

## Installation

```bash
pip install ing_theme_matplotlib
```

## Usage

You can use the dark Matplotlib style theme in the following way:

```python
from ing_theme_matplotlib import mpl_style
```
```python
mpl_style(dark=True)
```

And to use the light Matplotlib style theme, you can do the following: 

```python
from ing_theme_matplotlib import mpl_style
```
```python
mpl_style(dark=False)
```
> ⚠️ Make sure to run `from ing_theme_matplotlib import mpl_style` and `mpl_style()` in **different cells** as shown above. See [this issue](https://github.com/jupyter/notebook/issues/3691).

## Adding ING Logo

Assume that below is the function we use for plotting;

```python
def line_plot(ax):
    rng = np.random.RandomState(4)
    x = np.linspace(0, 10, 500)
    y = np.cumsum(rng.randn(500, 4), 0)
    ax.set_title('Line Graph')
    ax.set_xlabel('— Time')
    ax.set_ylabel('— Random values')
    ax.plot(x, y, label = ['Bitcoin', 'Ethereum', 'Dollar', 'Oil'])
    ax.legend(['Bitcoin', 'Ethereum', 'Dollar', 'Oil'], loc = 1, fontsize = 'medium')
    ax.set_xlim([0, 10])
    ax.set_ylim([-20, 60])
    ax.figure.set_figwidth(16)
    ax.figure.set_figheight(8)
    ax.spines['right'].set_position(('axes', 1.05))
    ax.spines['right'].set_color('none')
```

You can add the default ing logo to your plot by calling add_logo function inside the plotting function.

```python
from ing_theme_matplotlib.mpl_style import add_logo
```
```python
mpl_style()
line_plot(add_logo())
```

![png](https://gitlab.com/ing_rpaa/ing_theme_matplotlib/uploads/0ac070fd674120ef8af60047b90e6018/line_dark_ing_logo.png)

You can also add custom logos to your plot by giving the path where the image is located.

```python
from ing_theme_matplotlib.mpl_style import add_logo
```
```python
mpl_style(dark = False)
line_plot(add_logo(bottom_left = 'ing_theme_matplotlib/logos/RPAA_Logo_RGB_Line.png'))
```

![png](https://gitlab.com/ing_rpaa/ing_theme_matplotlib/uploads/16c46cc17fc9e3492cf09bf9433d1c43/line_light_custom_logo.png)

For more examples see [`ExamplePlots.ipynb`](ExamplePlots.ipynb).

## Supported chart types

- Line plots
- Scatter plots
- Bubble plots
- Bar charts
- Pie charts
- Histograms and distribution plots
- 3D surface plots
- Stream plots
- Polar plots

## What licence do we use?

ING Style plotting is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). 
`ing-theme-matplotlib` is forked from [qbstyles](https://github.com/quantumblacklabs/qbstyles).
