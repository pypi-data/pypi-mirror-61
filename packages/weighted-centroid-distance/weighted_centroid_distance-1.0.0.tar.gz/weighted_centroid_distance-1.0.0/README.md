<div align="center">
    <h1>Weighted Centroid Distance</h1>
</div>

A new model assessment technique for multi-class classification tasks in machine learning.

For the statistical theory, please see the white paper in `/paper`. It is auto
generated from `.tex` to `.pdf`.

## How to use

```python
# Python
from weighted_centroid_distance import WeightedCentroidDistance
distribution = WeightedCentroidDistance.get_distribution([1, 2, 3, 3, 4, 5, 5, 5], inverse=False)
wcd = WeightedCentroidDistance(distribution=distribution)
y____ = [1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5]
y_hat = [1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 1, 5, 5, 2]
res = wcd.get_distance(y=y____, y_hat=y_hat)
print("res: ", res)
# 0.12086457016125143
```

## Todo

- [ ] Create graphs for all parts of the algorithm defined in the paper
- [ ] Improve python script, and make a versions for other languages.
