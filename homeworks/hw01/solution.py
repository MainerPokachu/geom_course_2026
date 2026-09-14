import pathlib
import data_utils as du
import pandas as pd
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]

def main() -> None:
    
    #Пути файлов
    path1 = ROOT / "data/raw/hw01/wells.csv"
    path2 = ROOT / "data/raw/hw01/layers.xlsx"
    path3 = ROOT / "data/raw/hw01/pumping_test.txt"
    output_dir = ROOT / "data/processed/hw01"
    output_file1 = output_dir / "wells_clean.csv"
    output_file2 = output_dir / "table_summary.xlsx"
    result_txt = ROOT / "exports/hw01/result.txt"
    exports_dir = ROOT / "exports/hw01"
    
    #импорт таблиц в переменные
    wells = du.read_wells(path1)
    layers = du.read_layers(path2)
    pumping_test = du.read_pumping_test(path3)
    
    #Вывод информации о таблицах
    du.print_info(wells)
    du.print_info(layers)
    du.print_info(pumping_test)
    
    #Счёт пропусков и удаление строки с пропуском
    print(wells.isna().sum())
    wells_clean = wells.dropna(subset=["pressure_mpa"]).copy()
    
    #Проверка условий и сохранения обработанных данных
    assert (wells_clean["radius_m"] > 0).all()
    assert (layers["thickness_m"] > 0).all()
    assert layers["porosity_fraction"].between(0, 1).all()
    du.save_csv(output_dir, wells_clean, output_file1)
    
    #Добавление новых столбцов в wells_clean
    wells_clean["pressure_pa"] = wells_clean["pressure_mpa"] * 1_000_000
    wells_clean["pressure_difference_mpa"] = 12 - wells_clean["pressure_mpa"]
    wells_clean["relative_change_percent"] = wells_clean["pressure_difference_mpa"] / 12 * 100
    du.save_csv(output_dir, wells_clean, output_file1)
    
    #Проверка координат
    wells_clean["theta_rad"] = wells_clean["azimuth_deg"] * np.pi / 180
    wells_clean["x_check"] = wells_clean["radius_m"] * np.cos(wells_clean["theta_rad"])
    wells_clean["y_check"] = wells_clean["radius_m"] * np.sin(wells_clean["theta_rad"])
    
    #Сравнение с табличными
    assert np.allclose(wells_clean["x_m"], wells_clean["x_check"], atol=0.02)
    assert np.allclose(wells_clean["y_m"], wells_clean["y_check"], atol=0.02)
    
    #Логарифм
    wells_clean["log_radius"] = np.log(wells_clean["radius_m"])
    
    #Экспонента
    pumping_test["decay"] = np.exp(-pumping_test["time_h"] / 36)
    
    #Сохраняем все изменения в итоговые таблицы
    du.save_csv(output_dir, wells_clean, output_file1)
    du.save_xlsx(output_dir, pumping_test, output_file2)
    
    #Высчитываем и выводим требуемые характеристики
    table_summary = pd.DataFrame(
    {
        "pressure_mpa": [
            wells_clean["pressure_mpa"].min(),
            wells_clean["pressure_mpa"].max(),
            wells_clean["pressure_mpa"].mean(),
        ],
        "radius_m": [
            wells_clean["radius_m"].min(),
            wells_clean["radius_m"].max(),
            wells_clean["radius_m"].mean(),
        ],
        "thickness_m": [
            layers["thickness_m"].min(),
            layers["thickness_m"].max(),
            layers["thickness_m"].mean(),
        ],
        "porosity_fraction": [
            layers["porosity_fraction"].min(),
            layers["porosity_fraction"].max(),
            layers["porosity_fraction"].mean(),
        ],
    },
    index=["min", "max", "mean"]
    )
    
    #Вывод требуемых значений
    pressure = wells_clean["pressure_mpa"].to_numpy()
    print("First value: ", pressure[0])
    print("Last value: ",  pressure[-1])
    print("First 3 values: ", pressure[:3])
    print("Every second value: ", pressure[::2])
    mask = pressure < pressure.mean()
    selected = pressure[mask]
    print("First mask: ", selected)
    mask = wells_clean["radius_m"] > 100
    selected = wells_clean[mask]
    print("Second mask: ", selected)
    
    #Создание двумерного массива
    pressure_matrix = pumping_test[["boundary_pressure_mpa", "well_pressure_mpa"]
                                   ].to_numpy()
    du.print_matrix_info(pressure_matrix)
    
    #Создание трёхмерного массива
    experiment_1 = pressure_matrix
    experiment_2 = pressure_matrix + 0.05
    pressure_cube = np.stack([experiment_1, experiment_2], axis=0)
    print("first table: ", pressure_cube[0])
    print("Second table: ", pressure_cube[1])
    print("First row of first table: ", pressure_cube[0, 0])
    print("Pressure column: ", pressure_cube[:, :, 1])
    
    #Транспонирование
    pressure_transposed = pressure_matrix.T
    du.print_matrix_info(pressure_transposed)
    
    #Reshape
    flat = pressure_cube.reshape(-1)
    restored = flat.reshape(pressure_cube.shape)
    
    #Проверка
    assert np.allclose(restored, pressure_cube)
    
    #Класс
    wells_info = du.DatasetInfo("wells", wells)
    layers_info = du.DatasetInfo("layers", layers)
    pumping_info = du.DatasetInfo("pumping_test", pumping_test)

    print(wells_info.describe())
    print(layers_info.describe())
    print(pumping_info.describe())
    
    #Сохранение итоговых результатов
    du.save_csv(output_dir, wells_clean, output_file1)
    du.save_xlsx(output_dir, table_summary, output_file2)
    
    np.save(output_dir / "pressure_matrix.npy", pressure_matrix)
    matrix_loaded = np.load(output_dir / "pressure_matrix.npy")
    
    np.savez(output_dir / "pressure_cube.npz", pressure_cube=pressure_cube)
    cube_loaded = np.load(output_dir / "pressure_cube.npz")["pressure_cube"]
    
    assert np.allclose(pressure_matrix, matrix_loaded)
    assert np.allclose(pressure_cube, cube_loaded)

    exports_dir.mkdir(parents=True, exist_ok=True)
    with open(result_txt, "w", encoding="utf-8") as f:
        f.write(f"wells shape: {wells_clean.shape}\n")
        f.write(f"pressure_matrix shape: {pressure_matrix.shape}\n")
        f.write(f"pressure_cube shape: {pressure_cube.shape}\n\n")

        f.write("Min:\n")
        f.write(table_summary.loc["min"].to_string())
        f.write("\n\n")

        f.write("Max:\n")
        f.write(table_summary.loc["max"].to_string())
        f.write("\n\n")

        f.write("Mean:\n")
        f.write(table_summary.loc["mean"].to_string())
        f.write("\n")
    
if __name__ == "__main__":
    main()