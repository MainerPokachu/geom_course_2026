import pathlib
import data_utils as du
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
required_figures = [
    ROOT / "figures/hw02/pressure_over_time.svg",
    ROOT / "figures/hw02/pressure_by_radius.svg"
]
pumping_path = ROOT / "data/raw/hw01/pumping_test.txt"
wells_path = ROOT / "data/processed/hw01/wells_clean.csv"
output_dir = ROOT / "figures/hw03"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = ROOT / "homeworks/hw03"

def main():
    for path in required_figures:
        assert path.exists()
        assert path.stat().st_size > 0
    
    pumping_test = du.read_pumping_test(pumping_path)
    wells = du.read_wells(wells_path)
    
    assert pumping_test.shape == (13, 4)
    assert wells.shape[0] == 7
    assert not pumping_test.isna().any().any()
    assert not wells.isna().any().any()
    
    time_h = pumping_test["time_h"].to_numpy()
    boundary_pressure_mpa = pumping_test["boundary_pressure_mpa"].to_numpy()
    well_pressure_mpa = pumping_test["well_pressure_mpa"].to_numpy()
    
    well_id = wells["well_id"].to_numpy()
    radius_m = wells["radius_m"].to_numpy()
    observation_pressure_mpa = wells["pressure_mpa"].to_numpy()
    
    order = np.argsort(radius_m)
    well_id = well_id[order]
    radius_m = radius_m[order]
    observation_pressure_mpa = observation_pressure_mpa[order]
    
    pressure_drop_mpa = boundary_pressure_mpa - well_pressure_mpa
    observation_drop_mpa = 12.0 - observation_pressure_mpa
    
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8),
        constrained_layout=True
    )
    
    ax = axes[0, 0]
    
    ax.plot(
        time_h,
        boundary_pressure_mpa,
        marker="o",
        label="Давление на границе"
    )
    
    ax.plot(
        time_h,
        well_pressure_mpa,
        marker="s",
        label="Давление в скважине"
    )
    
    ax.set_title("A. Давление во времени")
    ax.set_xlabel("Время, ч")
    ax.set_ylabel("Давление, МПа")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    ax = axes[0, 1]
    
    sc = ax.scatter(
        radius_m,
        observation_pressure_mpa,
        c=observation_pressure_mpa,
        cmap="viridis",
        s=60
    )
    
    ax.set_title("B. Давление по радиусу")
    ax.set_xlabel("Радиус, м")
    ax.set_ylabel("Давление, МПа")
    
    fig.colorbar(
        sc,
        ax=ax,
        label="Давление, МПа"
    )
    
    ax = axes[1, 0]
    
    ax.bar(
        well_id,
        observation_drop_mpa
    )
    
    ax.set_title("C. Падение давления по скважинам")
    ax.set_xlabel("Идентификатор скважины")
    ax.set_ylabel("Падение давления, МПа")
    ax.grid(axis="y", alpha=0.3)
    
    ax = axes[1, 1]
    
    ax.boxplot(
        [
            boundary_pressure_mpa,
            well_pressure_mpa,
        ],
        tick_labels=[
            "На границе",
            "В скважине"
        ]
    )
    
    ax.set_title("D. Распределение давления")
    ax.set_ylabel("Давление, МПа")
    ax.grid(axis="y", alpha=0.3)
    
    fig2, axes2 = plt.subplots(
        1,
        2,
        figsize=(12, 5),
        constrained_layout=True
    )
    
    pressure_data = [
        boundary_pressure_mpa,
        well_pressure_mpa
    ]
    
    labels = [
        "Давление на границе",
        "Давление в скважине"
        ]
    
    axes2[0].boxplot(
        pressure_data,
        tick_labels=labels,
    )
    axes2[0].set_title("A. Boxplot")
    axes2[0].set_ylabel("Давление, МПа")
    axes2[0].grid(axis="y", alpha=0.3)
    
    axes2[1].violinplot(
        pressure_data,
        showmedians=True
    )
    axes2[1].set_xticks([1, 2])
    axes2[1].set_xticklabels(labels)
    axes2[1].set_title("B. Violin plot")
    axes2[1].set_ylabel("Давлени, МПа")
    axes2[1].grid(axis="y", alpha=0.3)
    
    fig.savefig(
        output_dir / "pressure_overview.png",
        dpi = 200,
        bbox_inches = "tight"
    )
    
    fig.savefig(
        output_dir / "pressure_overview.svg",
        bbox_inches = "tight"
    )
    
    fig2.savefig(
        output_dir / "distributions.png",
        dpi = 200,
        bbox_inches = "tight"
    )
        
    fig2.savefig(
        output_dir / "distributions.svg",
        bbox_inches = "tight"
    )
    
    plt.close(fig)
    plt.close(fig2)
    
    np.savez(
        output_path / "viz_data.npz",
        time_h=time_h,
        boundary_pressure_mpa=boundary_pressure_mpa,
        well_pressure_mpa=well_pressure_mpa,
        pressure_drop_mpa=pressure_drop_mpa,
        well_id=well_id,
        radius_m=radius_m,
        observation_pressure_mpa=observation_pressure_mpa,
        observation_drop_mpa=observation_drop_mpa
    )
    
    data_loaded = np.load(output_path / "viz_data.npz", allow_pickle=True)
    expected_keys = {
        "time_h",
        "boundary_pressure_mpa",
        "well_pressure_mpa",
        "pressure_drop_mpa",
        "well_id",
        "radius_m",
        "observation_pressure_mpa",
        "observation_drop_mpa",
    }
    
    assert set(data_loaded.files) == expected_keys
    original_data = {
        "time_h": time_h,
        "boundary_pressure_mpa": boundary_pressure_mpa,
        "well_pressure_mpa": well_pressure_mpa,
        "pressure_drop_mpa": pressure_drop_mpa,
        "well_id": well_id,
        "radius_m": radius_m,
        "observation_pressure_mpa": observation_pressure_mpa,
        "observation_drop_mpa": observation_drop_mpa,
    }

    for key, original in original_data.items():
        loaded = data_loaded[key]

        assert loaded.shape == original.shape, f"Неверная форма: {key}"
        assert np.array_equal(loaded, original), f"Значения не совпадают: {key}"

    data_loaded.close()

    print("Все проверки пройдены!")
    
if __name__ == "__main__":
    main()