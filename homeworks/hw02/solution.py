import pathlib
import pandas as pd
import plot_utils as pu

ROOT = pathlib.Path(__file__).resolve().parents[2]
test_path = ROOT / "data/raw/hw01/pumping_test.txt"
figure_path = ROOT / "figures/hw02"

def main():
    
    pu.read_tests(ROOT / "data/raw/hw01/pumping_test.txt")
    figure_path.mkdir(parents=True, exist_ok=True)
    pumping_test = pu.read_tests(test_path)
    pu.plot_pressure_over_time(pumping_test, figure_path)
    
    wells_clean = pu.read_wells(ROOT / "data/processed/hw01/wells_clean.csv")
    wells_sorted = wells_clean.sort_values("radius_m")
    assert (wells_sorted["radius_m"] > 0).all()
    pu.plot_pressure_by_radius(wells_sorted, figure_path)
    
    assert (figure_path / "pressure_over_time.png").exists()
    assert (figure_path / "pressure_over_time.svg").exists()
    assert (figure_path / "pressure_by_radius.png").exists()
    assert (figure_path / "pressure_by_radius.svg").exists()
    
    print("Работа программы завершена успешно")
    
if __name__ == "__main__":
    main()