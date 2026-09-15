import pandas as pd
import matplotlib.pyplot as plt

def read_tests(path):
    data_frame = pd.read_csv(path, sep="\t")
    return data_frame

def read_wells(path):
    data_frame = pd.read_csv(path)
    return data_frame

def plot_pressure_over_time(table, output_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        table["time_h"],
        table["boundary_pressure_mpa"],
        marker = "o",
        color = "blue",
        label = "Давление на границе")
    
    ax.plot(
        table["time_h"],
        table["well_pressure_mpa"],
        marker = "o",
        color = "red",
        label = "Давление в скважине"
    )
    
    ax.set_title("Изменение давления во времени")
    ax.set_xlabel("Время, ч")
    ax.set_ylabel("Давление, МПа")
    ax.legend()
    ax.grid(alpha = 0.3)
    fig.tight_layout()
    
    min_index = table["well_pressure_mpa"].idxmin()
    min_time = table.loc[min_index, "time_h"]
    min_pressure = table.loc[min_index, "well_pressure_mpa"]
    
    ax.annotate(
        f"{min_pressure:.2f} МПа",
        xy = (min_time, min_pressure),
        xytext=(-25, 5),
        textcoords="offset points"
    )
    
    fig.savefig(
        output_dir / "pressure_over_time.png",
        dpi = 200,
        bbox_inches = "tight"
    )
    
    fig.savefig(
        output_dir / "pressure_over_time.svg",
        bbox_inches = "tight"
    )
    
    plt.close(fig)
    
def plot_pressure_by_radius(table, output_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        table["radius_m"],
        table["pressure_mpa"],
        linestyle = "none",
        marker = "o"
    )
    ax.set_xscale("log")
    ax.set_title("Давление в наблюдательных скважинах")
    ax.set_xlabel("Расстояние, м")
    ax.set_ylabel("Давление, МПа")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    
    fig.savefig(
            output_dir / "pressure_by_radius.png",
            dpi = 200,
            bbox_inches = "tight"
        )
        
    fig.savefig(
            output_dir / "pressure_by_radius.svg",
            bbox_inches = "tight"
        )
    
    plt.close(fig)