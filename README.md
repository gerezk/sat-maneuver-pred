## Background

This project aims to develop a model that learns the maneuver pattern-of-life (PoL) of satellites using two-line element set (TLE) data and predicts future maneuvers. Some satellite operators do not notify the space community of upcoming maneuvers, making it crucial for space domain awareness (SDA) analysts to anticipate these movements.

The model could help SDA analysts in sensor tasking. For maneuvers within the established PoL, SDA sensors can be tasked to increase collection efforts around predicted maneuvers to quickly determine the satellite's post-maneuver orbit. For unexpected maneuvers outside the PoL, analysts may want to increase collection following the maneuver to assess potential anomalies or unusual activity.

## Getting Started

1. Create a python virtual environment

```sh
python3 -m venv .venv
```

2. Activate virtual environment 

- Mac / Linux

```sh
source .venv/bin/activate
```

- Windows

```sh
.venv\Scripts\activate
```

3. Install requirements

```sh
pip install -r requirements.txt
```
