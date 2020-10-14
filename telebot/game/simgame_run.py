import os
from game import schedule_read
import subprocess
import time
from game import data_extractor as de
import rips
import glob
import os
from PIL import Image
import plotly.graph_objects as go
import pandas as pd
import plotly
from plotly.offline import plot_mpl


def start(this_team_name):
    current_dir = os.getcwd()
    run_sim_option = True
    if run_sim_option:

        print("---Импорт решений " + this_team_name + '---')
        schedule_read.create_schedule_for_team(this_team_name)

        print("---Перемешsение сгенерированной schedule секции для команды " + this_team_name + '---')
        path_to_generated_schedule = "game/dataspace/" + this_team_name + '/'
        new_schedule_file_name = "schedule_new_" + this_team_name + ".inc"
        abs_path_to_new_schedule = path_to_generated_schedule + new_schedule_file_name
        subprocess.call(["cp", "-r" , abs_path_to_new_schedule, 'game/workspace/spe1_SCH.INC'])

        print("---Запуск симулятора для команды " + this_team_name + '---')
        path_to_opm_data = current_dir+ "/game/workspace"
        os.chdir(path_to_opm_data)
        #result = os.system("mpirun -np 2 flow spe1.DATA")

        print("---Запуск скрипта на python3.8 для извлечения результатов команды " + this_team_name + '---')
        os.chdir(current_dir)
        os.system("python3.8 game/data_extractor.py")

        print("---Перенос результатов в папку команды " + this_team_name + '---')
        if not os.path.isdir(f"game/resultspace/{this_team_name}"):
            os.mkdir(f"game/resultspace/{this_team_name}")
        subprocess.call(["cp", "-r" , 'game/sim_result.csv', f'game/resultspace/{this_team_name}'])

        print("---Отправка результатов пользователю---")
        de.export_to_csv(current_dir, this_team_name)
        #export_snapshots(this_team_name)
        fig_snapshots(this_team_name)


def export_snapshots(name):
    path_grid = 'game/workspace/SPE1'
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
        
def fig_snapshots(name):
    path_grid = 'game/workspace/SPE1'
    process = subprocess.Popen('exec ResInsight --case "%s.SMSPEC"' % path_grid, shell=True)
    time.sleep(5)
    resinsight = rips.Instance.find()
    dirname = f'game/workspace/snapshots/{name}'
       # Get a list of all plots
    plots = resinsight.project.plots()
    resinsight.set_export_folder(export_type='SNAPSHOTS', path=dirname)
    
    for plot in plots:
        plot.export_snapshot(export_folder=dirname)
        plot.export_snapshot(export_folder=dirname, output_format='PNG')
        if isinstance(plot, rips.WellLogPlot):
        	plot.export_data_as_las(export_folder=dirname)
        	plot.export_data_as_ascii(export_folder=dirname)
    
    process.kill()
    
    