# capetools 🕶
> A set of python 🐍 tools to process and model PV


I put together a set of tools used to clean data and model bifacial systems using [pvfactors](http://github.com/SUNPOWER/pvfactors), [pvlib](https://github.com/pvlib/pvlib-python) and [bifacialvf](http://bifacialvf) 🌞

## Install

As of 02/2019: [bifacialvf](https://github.com/NREL/bifacialvf) has not yet merged this [PR](https://github.com/NREL/bifacialvf/pull/25), the simulate function cannot take arbitrary metereological data on the form of pandas DataFrames. So we are force to install a custom fork of bifacialvf from [here](https://github.com/tcapelle/bifacialvf/p). This is way, a formal release of capetools to PyPI is not possible rght now, so we have to install by cloning from github.

The recommended method is to install capetools on a conda envirnment. Ideally create a `conda env` with `python 3.6` and then clone and install using pip.

`conda create --name=your_env_name python=3.7`

`git clone https://github.com/tcapelle/capetools/`

go inside the cloned capetools repo and do:

`pip install .`

or on editable mode, git clone this repo, and from within the repo install using:

`pip install -e .`

## Getting started 💪

```python
from capetools.imports import *
from capetools.utils.missing import *
from capetools.utils.tmy import read_pvgis
from capetools.modelling.mypvfactors import *
from capetools.modelling.mybifacialvf import *
```

```python
PATH = Path.cwd().parent/'data'
fname = PATH/'pvgis_tmy_chambery.csv'
```

We will ingest a PVGIS downloaded file for Chambery

```python
gps_data, months, tmy_data = read_pvgis(fname)
```

```python
tmy_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>temp</th>
      <th>humidity</th>
      <th>ghi</th>
      <th>dni</th>
      <th>dhi</th>
      <th>infra</th>
      <th>ws</th>
      <th>wd</th>
      <th>pressure</th>
    </tr>
    <tr>
      <th>time(UTC)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2012-01-01 00:00:00</th>
      <td>2.87</td>
      <td>88.28</td>
      <td>0.0</td>
      <td>-0.0</td>
      <td>0.0</td>
      <td>259.63</td>
      <td>1.33</td>
      <td>170.0</td>
      <td>99504.0</td>
    </tr>
    <tr>
      <th>2012-01-01 01:00:00</th>
      <td>3.59</td>
      <td>90.07</td>
      <td>0.0</td>
      <td>-0.0</td>
      <td>0.0</td>
      <td>268.30</td>
      <td>1.39</td>
      <td>166.0</td>
      <td>99508.0</td>
    </tr>
    <tr>
      <th>2012-01-01 02:00:00</th>
      <td>4.32</td>
      <td>91.86</td>
      <td>0.0</td>
      <td>-0.0</td>
      <td>0.0</td>
      <td>276.97</td>
      <td>1.45</td>
      <td>162.0</td>
      <td>99511.0</td>
    </tr>
    <tr>
      <th>2012-01-01 03:00:00</th>
      <td>5.04</td>
      <td>93.64</td>
      <td>0.0</td>
      <td>-0.0</td>
      <td>0.0</td>
      <td>285.64</td>
      <td>1.51</td>
      <td>167.0</td>
      <td>99517.0</td>
    </tr>
    <tr>
      <th>2012-01-01 04:00:00</th>
      <td>5.76</td>
      <td>95.43</td>
      <td>0.0</td>
      <td>-0.0</td>
      <td>0.0</td>
      <td>294.32</td>
      <td>1.57</td>
      <td>171.0</td>
      <td>99524.0</td>
    </tr>
  </tbody>
</table>
</div>



We can quickly look at missing data:

```python
plot_missing(tmy_data)
```


![png](docs/images/output_17_0.png)


as expected, no missing data !

## Simulations

### pvfactors

```python
params = system_def(n_pvrows=3); params
```




    {'n_pvrows': 3,
     'pvrow_height': 1.6218180900789148,
     'pvrow_width': 2.02,
     'tracking': False,
     'axis_azimuth': 0,
     'surface_tilt': 38,
     'surface_azimuth': 180,
     'albedo': 0.4,
     'gcr': 0.5,
     'rho_front_pvrow': 0.075,
     'rho_back_pvrow': 0.075,
     'cut': {0: {'front': 1, 'back': 7},
      1: {'front': 1, 'back': 7},
      2: {'front': 1, 'back': 7}}}



```python
data = get_data(fname, params)
```

```python
pvarray = run_pvfactors_simulation(data, params)
```

    /home/tc256760/anaconda3/envs/fastai/lib/python3.7/site-packages/pvfactors/viewfactors/vfmethods.py:181: RuntimeWarning: invalid value encountered in true_divide
      vf_pvrow_to_gnd_surf * pvrow_surf_length / gnd_surf_length, 0.)
    /home/tc256760/anaconda3/envs/fastai/lib/python3.7/site-packages/pvfactors/viewfactors/vfmethods.py:181: RuntimeWarning: divide by zero encountered in true_divide
      vf_pvrow_to_gnd_surf * pvrow_surf_length / gnd_surf_length, 0.)
    /home/tc256760/anaconda3/envs/fastai/lib/python3.7/site-packages/pvfactors/viewfactors/vfmethods.py:531: RuntimeWarning: divide by zero encountered in true_divide
      vf_1_to_2 = (d1 + d2 - l1 - l2) / (2. * width)
    /home/tc256760/anaconda3/envs/fastai/lib/python3.7/site-packages/pvfactors/viewfactors/vfmethods.py:531: RuntimeWarning: invalid value encountered in true_divide
      vf_1_to_2 = (d1 + d2 - l1 - l2) / (2. * width)
    /home/tc256760/anaconda3/envs/fastai/lib/python3.7/site-packages/pvfactors/viewfactors/vfmethods.py:607: RuntimeWarning: invalid value encountered in true_divide
      vf_1_to_2 = np.abs(sum_2 - sum_1) / (2. * width_1)
    /home/tc256760/anaconda3/envs/fastai/lib/python3.7/site-packages/pvfactors/viewfactors/vfmethods.py:222: RuntimeWarning: invalid value encountered in true_divide
      vf_i_to_j * length_i / length_j, 0.)


```python
ax = plot_idx(pvarray)
ax.set_xlim(-2, 10)
```




    (-2, 10)




![png](docs/images/output_24_1.png)


```python
res_pvfactors = individual_report(pvarray, index=data.index)
```

```python
res_pvfactors.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>qinc_0</th>
      <th>qinc_1</th>
      <th>qinc_2</th>
      <th>qinc_3</th>
      <th>qinc_4</th>
      <th>qinc_5</th>
      <th>qinc_6</th>
      <th>qinc_front</th>
      <th>qinc_back</th>
    </tr>
    <tr>
      <th>time(UTC)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-01 00:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2019-01-01 01:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2019-01-01 02:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2019-01-01 03:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2019-01-01 04:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



```python
res_pvfactors['21 June 2019'].plot();
```


![png](docs/images/output_27_0.png)


### bifacialvf

```python
res_bifacialvf = run_bifacialvf_simulation(data)
```

      0%|          | 0/8760 [00:00<?, ?it/s]/home/tc256760/Apps/bifacialvf/bifacialvf/vf.py:300: RuntimeWarning: divide by zero encountered in double_scalars
      projectedX2 = PcellX + np.float64(PcellY) / math.tan(startElvDown);      # Projection of ElvDown to ground in +x direction (X1 and X2 opposite nomenclature for front irradiance method)
      0%|          | 40/8760 [00:00<00:22, 379.91it/s]

     
    ********* 
    Running Simulation for TMY3:  Chambery
    Location:   Chambery
    Lat:  45.637001  Long:  5.881  Tz  -1.0
    Parameters: beta:  0   Sazm:  180   Height:  0.5   rtr separation:  8.0   Row type:  interior   Albedo:  0.4
    Saving into output.csv
     
     


    100%|██████████| 8760/8760 [00:27<00:00, 314.85it/s]

    Finished


    


```python
res_bifacialvf['21 June 2019'].plot();
```


![png](docs/images/output_30_0.png)


## Coontributing 👇
Read [nbdev](http://github.com/fastai/nbdev) documentation please.
