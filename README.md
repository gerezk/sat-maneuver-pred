## Background

This project aims to develop a model that learns the maneuver pattern-of-life (PoL) of satellites using element set (ELSET) data and predicts future maneuvers. Some satellite operators do not notify the space community of upcoming maneuvers, making it crucial for space domain awareness (SDA) analysts to anticipate these movements.

The model could help SDA analysts in sensor tasking. For maneuvers within the established PoL, SDA sensors can be tasked to increase collection efforts around predicted maneuvers to quickly determine the satellite's post-maneuver orbit. For unexpected maneuvers outside the PoL, analysts may want to increase collection following the maneuver to assess potential anomalies or unusual activity.

## Getting Started

Conda is required since orekit is used for propagating ELSETs; the library is most easily accessible from conda-forge.

1. Create a conda environment

```sh
conda env create --file environment.yml
```

2. Activate the environment

```sh
conda activate sat_pred
```

3. Install orekit from conda-forge

```sh
conda install -c conda-forge orekit
```

4. Download Orekit data as a library using pip

```sh
pip install git+https://gitlab.orekit.org/orekit/orekit-data.git
```