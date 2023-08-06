# supervenn: visualize relations of multiple sets in Python using matplotlib

### Installation
`pip install supervenn`

### Dependencies
- `numpy`
- `matplotlib` at least version 3.0.3

### Basic usage 
The main entry point is the eponymous supervenn function, that takes a list of python `set`s as its first and only
required argument:
```python
from supervenn import supervenn
sets = [{1, 2, 3, 4}, {3, 4, 5}, {1, 5, 6}]
supervenn(sets, side_plots=False)
```
<img src="https://i.imgur.com/dHr8snl.png" width=400>

Each row is a set, the order from bottom to top is the same as in the `sets` list. 

The numbers at the bottom show the sizes (cardinalities) of all intersections, aka **chunks**. The sizes of sets and
their intersections (chunks) are up to proportion.

The algorithm automatically chooses an order of the chunks (the colimns of the array plotted) to minimize the number of
parts, in which the sets are broken. As you can see, there is only one gap inside all rows, namely in the blue set. This
is achieved using a quasi-greedy optimization algorithm with randomization.

By default, additional *side plots* are also displayed:

```python
supervenn(sets)
```
<img src="https://i.imgur.com/4kDKSGs.png" width=400>
Here, the numbers on the right are the set sizes (cardinalities), and numbers on the top show how many sets does this
intersection make part of. The grey bars underneath represent the same numbers visually.

### Most important arguments
- `set_annotations`: names to be displayed in each row instead of `Set_0`, `Set_1` etc.
- `figsize`: the figure size in inches; calling `plt.figure(figsize=(16, 10))` and `supervenn` afterwards
 will not work, because the function makes its own figure. **TODO**: dpi
- `side_plots`: `True` (default) or `False`, as shown above.
- `sets_ordering`: `None` (default - keep the order of sets as passed into function), `'minimize gaps'` (use same
quasi-greedy algorithm to group similar sets closer together), `'size'`(bigger sets go first), `'chunk count'` (sets
that contain most chunks go first), `'random'`.
- `widths_minmax_ratio`: `None` (default) or a number `0 < r <= 1`. Useful in case the chunks (intersections) are very
different in sizes. Will map the chunk sizes according to `w -> a * w + b` so that the minimal to maximal chunk width
ratio is no smaller than `widths_minmax_ratio`. The exact proportionality is lost in this case. Setting
`widths_minmax_ratio=1` will result in all chunks being displayed as same size (no proportionalty at all.)
- `col_annotations_ys_count`: 1 (default), 2, or 3 - also helps to reduce clutter in column annotations area.

Other arguments can be found in the docstring to the function.

### Less trivial example #1: words of different categories

```python
letters = {'a', 'r', 'c', 'i', 'z'}
programming_languages = {'python', 'r', 'c', 'c++', 'java', 'julia'}
animals = {'python', 'buffalo', 'turkey', 'cat', 'dog', 'robin'}
geographic_places = {'java', 'buffalo', 'turkey', 'moscow'}
names = {'robin', 'julia', 'alice', 'bob', 'conrad'}
green_things = {'python', 'grass'}
sets = [letters, programming_languages, animals, geographic_places, names, green_things]
labels = ['letters', 'programming languages', 'animals', 'geographic places',
          'human names', 'green things']
supervenn(sets, set_annotations=labels)
```
<img src="https://i.imgur.com/9Or2HwK.png" width=550>

### Less trivial example #2: banana genome.
[Data courtesy of Jake R Conway, Alexander Lex, Nils Gehlenborg - creators of UpSet](https://github.com/hms-dbmi/UpSetR-paper/blob/master/bananaPlot.R)

Image from [D’Hont, A., Denoeud, F., Aury, J. et al. The banana (Musa acuminata) genome and the evolution of monocotyledonous plants](https://www.nature.com/articles/nature11241)

Figure from original article (note that it is by no means proportional!):

<img src="https://i.imgur.com/iQlcLVG.jpg" width=700>

Figure made with [UpSetR](https://caleydo.org/tools/upset/)

<img src="https://i.imgur.com/DH72eJJ.png" width=700>

Figure made with supervenn (using the `widths_minmax_ratio` argument)

```python
supervenn(sets_list, species_names, figsize=(20, 10), widths_minmax_ratio=0.1,
          sets_ordering='minimize gaps', rotate_col_annotations=True, col_annotations_area_height=1.2)
```
<img src="https://i.imgur.com/1FGvOLu.png" width=850>

It must be noted that `supervenn` produces best results when there is some inherent structure to the sets in question.
This typically means that the number of non-empty intersections is significantly lower than the maximum possible
(which is `2^n_sets - 1`). This is not the case in the present case, as 62 of the 63 intersections are non-empty, and
hence the results are not that pretty.

### Less trivial example #3: order IDs in a vehicle routing problem solver tasks.
This was actually my motivation in creating this package. The [team I'm currently working in](https://yandex.ru/routing/)
provides an API that solves a variation of the Multiple Vehicles Routing Problem. The API solves tasks of the form
"Given 1000 delivery orders each with lat, lon, time window and weight, and 50 vehicles each with capacity and work
shift, distribute the orders between the vehicles and build an optimal route for each vehicle". 

A given client can send tens of such requests per day and sometimes it is usefult to look at their requests and
understand how they are related to each other in terms of what orders are included in each of the request. Are they
sending the same task over and over again  - a sign that they are not satisfied with routes they get and they might need
our help in using the API? Are they manually editing the routes (a process that results in more requests to our API, with
only the orders from affected routes included)? Or are they solving for several independent order sets and are happy
with each individual result?

Here's an example of a client who is not that happy:

<img src="https://i.imgur.com/9YfRC61.png" width=800>

Rows from bottom to top are requests to our API from earlier to later, represented by their sets of order IDs. With the
help of some custom annotations (`set_annotations` argument), the situation is immediately made clear. The client solved
a big task at 10:54, they were not happy about the result, and tried some manual edits until 11:11. Then in the evening
they re-sent the whole task twice over, probably with some change in parameters.

Another unhappy customer:

<img src="https://i.imgur.com/cGgCroA.png" width=800>

This guy here spend almost two hours, 17:40 to 19:30 solving the same full task over and over again, with some manual
edits in between. Looks like they might be doing something wrong and our help is needed.

And finally, a happy one:

<img src="https://i.imgur.com/E2o2ela.png" width=800>
Solved three unrelated tasks, was happy with all the three (no repeated requests, no manual edits; each order is
distributed only once).

### Algorithm used to minimize the gaps in the sets
The description of the algorithm can be found in the docstring to `supervenn._algorithms` module.


### Related work

#### [matplotlib-venn package](https://github.com/konstantint/matplotlib-venn) 
This tool plots proper area-propriotional Venn diagrams with circles for two or three sets. But the problem with circles
is that they are pretty useless even in the case of three sets. For example, if one set is symmetrical difference of the
other two:
```python
from matplotlib_venn import venn3
set_1 = {1, 2, 3, 4}
set_2 = {3, 4, 5}
set_3 = set_1 ^ set_2
venn3([set_1, set_2, set_3], set_colors=['steelblue', 'orange', 'green'], alpha=0.8)
```
<img src="https://i.imgur.com/Mijyzj8.png" width=260>

See all that zeros? This image makes little sense. The `supervenn`'s approach to this problem is to allow the sets to be
broken into separate parts, while trying to minimize the number of such breaks and guaranteeing exact proportionality of
all parts:

<img src="https://i.imgur.com/e3sMQrO.png" width=400>


#### [UpSetR and pyUpSet](https://caleydo.org/tools/upset/)
<img src="https://raw.githubusercontent.com/ImSoErgodic/py-upset/master/pictures/basic.png" width=800>
This approach, while very powerful, is less visual, as it displays, so to say only *statistics about* the sets, not the
sets in flesh.

### Author
This package is created and maintained by Fedor Indukaev. This is my first attempt at making a full Python package, so
it there may be some flaws or bad practices.  Any bug reports, comments, recommendations, feature requests,
pull requets, code reviews etc are most welcome. You can reach me at `my github username at mail by g0ogIe`.