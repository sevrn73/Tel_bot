import os
import schedule_read
import subprocess
import time
import data_extractor as de
import rips
import glob
import os
from PIL import Image


def start(this_team_name):
    current_dir = os.getcwd()
    run_sim_option = True
    if run_sim_option:

        print("---Импорт решений " + this_team_name + '---')
        schedule_read.create_schedule_for_team(this_team_name)

        print("---Перемешsение сгенерированной schedule секции для команды " + this_team_name + '---')
        path_to_generated_schedule = "dataspace/" + this_team_name + '/'
        new_schedule_file_name = "schedule_new_" + this_team_name + ".inc"
        abs_path_to_new_schedule = path_to_generated_schedule + new_schedule_file_name
        subprocess.call(["cp", "-r" , abs_path_to_new_schedule, 'workspace/spe1_SCH.INC'])

        print("---Запуск симулятора для команды " + this_team_name + '---')
        path_to_opm_data = current_dir+ "/workspace"
        os.chdir(path_to_opm_data)
        result = os.system("mpirun -np 2 flow spe1.DATA")

        print("---Запуск скрипта на python3.8 для извлечения результатов команды " + this_team_name + '---')
        os.chdir(current_dir)
        os.system("python3.8 data_extractor.py")

        print("---Перенос результатов в папку команды " + this_team_name + '---')
        if not os.path.isdir(f"resultspace/{this_team_name}"):
            os.mkdir(f"resultspace/{this_team_name}")
        command_to_move_results = "mv -f ./sim_result.csv ./resultspace/" + this_team_name + '/'
        os.system(command_to_move_results)

        print("---Экспорт решений в гугл таблицу  " + this_team_name + '---')
        de.export_to_csv(current_dir, this_team_name)
        time.sleep(2)
        export_snapshots(this_team_name)


def export_snapshots(name):
    path_grid = 'workspace/SPE1'
    process = subprocess.Popen('exec ResInsight --case "%s.EGRID"' % path_grid, shell=True)
    time.sleep(5)
    resinsight = rips.Instance.find()
    case = resinsight.project.cases()[0]
    resinsight.set_main_window_size(width=400, height=150)
    property_list = ['PRESSURE', 'SOIL']
    case_path = case.file_path
    folder_name = os.path.dirname(case_path)

    dirname = os.path.join(folder_name, f"snapshots/{name}")

    if os.path.exists(dirname) is False:
        os.mkdir(dirname)

    print("Exporting to folder: " + dirname)
    resinsight.set_export_folder(export_type='SNAPSHOTS', path=dirname)

    view = case.views()[0]
    time_steps = case.time_steps()
    l = len(time_steps) - 1
    for property in property_list:
        view.apply_cell_result(result_type='DYNAMIC_NATIVE', result_variable=property)
        view.set_time_step(time_step = l)
        view.export_snapshot()

    process.kill()

    images = []
    image_paths = glob.glob(dirname + '/*')

    for path in image_paths:
        images.append(Image.open(path))