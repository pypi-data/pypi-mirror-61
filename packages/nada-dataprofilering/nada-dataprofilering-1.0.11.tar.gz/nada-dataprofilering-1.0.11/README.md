# nada-dataprofilering
Python package that generates sql scripts for data profiling + connectors.

# Columns Metrics
Each metric function computes generate script that computes a metric and updates the value in NADA_PROFILERING_PROD.

The implemented metrics are

## Standard metrics
`standard_metric_functions.py`

| Metric                  | Function name    | Comments |
|-------------------------|------------------|----------|
|Number of observations   |num_rows          |          |
|Number of nulls          |num_nulls         |          |
|Number of nulls %        |num_nulls_pct     |          |
|Number of unique values  |count_unique      |          |
|Number of unique values %|count_unique_pct  |          |


## Number metrics
`number_metric_functions.py`

### Quantile metrics

| Metric                  | Function name    |Comments                      |
|-------------------------|------------------|------------------------------|
|Min                      |number_min        |                              |
|`p-th` percentile        |number_quantile   | Takes percentile as input    |
|Max                      |number_max        |                              |
|Range                    |number_range      |                              |
|Interquartile range      |number_iqr        |                              |

### Descriptive metrics

| Metric                  | Function name    |Comments  |
|-------------------------|------------------|----------|
|Standard deviation       |number_std        |          |
|Coef of variation        |number_cov        |          |
|Kurtosis                 |number_kurtosis   |          |
|Mean                     |number_mean       |          |
|MAD                      |number_mad        |          |
|Skewness                 |number_skewness   |          |
|Sum                      |number_sum        |          |
|Variance                 |number_variance   |          |
|Number of zero           |number_zero       |          |


## Date metrics
`date_metric_functions.py`

| Metric                  | Function name    |Comments  |
|-------------------------|------------------|----------|
|Min                      |date_min          |          |
|Median                   |date_median       |          |
|Max                      |date_max          |          |


## varchar2 metrics
`varchar2_metric_functions.py`

### Quantile metrics

| Metric                  | Function name    |Comments  |
|-------------------------|------------------|----------|
|Min length               |varchar2_min      |          |
|Median length            |varchar2_median   |          |
|Max length               |varchar2_max      |          |

### Descriptive metrics
| Metric                     | Function name    |Comments  |
|----------------------------|------------------|----------|
|Mean length                 |varchar2_mean     |          |
|Standard deviation length   |varchar2_std      |          |
