import os
import xlrd
from datetime import datetime, timedelta
from pprint import pprint

DATA_DIR = r'C:\Users\huiwa\MATLAB\HeartRateVariability\data\LWP2'

def get_task_timing(subj, task_id):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', 'timing']) + '.xlsx')
    workbook = xlrd.open_workbook(fp)
    sheet = workbook.sheet_by_name('In Lab')
    lab_date = sheet.cell(4, 1)
    task_start_t_excel = sheet.cell(5 + task_id, 1)
    task_start_t = excel_datetime_to_dt(workbook.datemode, lab_date, task_start_t_excel)
    task_end_t_excel = sheet.cell(6 + task_id, 1)
    task_end_t = excel_datetime_to_dt(workbook.datemode, lab_date, task_end_t_excel)
    return task_start_t.timestamp(), task_end_t.timestamp()

def get_task_timing_all(subj):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', 'timing']) + '.xlsx')
    workbook = xlrd.open_workbook(fp)
    sheet = workbook.sheet_by_name('In Lab')
    lab_date = sheet.cell(4, 1)
    timings = []
    for i in range(1, 20):
        t_excel = sheet.cell(5 + i, 1)
        py_dt = excel_datetime_to_dt(workbook.datemode, lab_date, t_excel)
        timings.append(py_dt.timestamp())
    #print(timings)
    return timings

def get_lab_start_end_time(subj):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', 'timing']) + '.xlsx')
    workbook = xlrd.open_workbook(fp)
    sheet = workbook.sheet_by_name('In Lab')
    lab_date = sheet.cell(4, 1)
    lab_start_t_excel = sheet.cell(5, 1)
    lab_start_t = excel_datetime_to_dt(workbook.datemode, lab_date, lab_start_t_excel)
    lab_end_t_excel = sheet.cell(24, 1)
    lab_end_t = excel_datetime_to_dt(workbook.datemode, lab_date, lab_end_t_excel)
    return lab_start_t.timestamp(), lab_end_t.timestamp()

def get_multi_task_time(subj, start_task_id, end_task_id):
    subj_dir = os.path.join(DATA_DIR, subj)
    fp = os.path.join(subj_dir, '_'.join([subj, 'lab', 'timing']) + '.xlsx')
    workbook = xlrd.open_workbook(fp)
    sheet = workbook.sheet_by_name('In Lab')
    lab_date = sheet.cell(4, 1)
    start_t_excel = sheet.cell(6 + start_task_id - 1, 1)
    start_t = excel_datetime_to_dt(workbook.datemode, lab_date, start_t_excel)
    end_t_excel = sheet.cell(6 + end_task_id, 1)
    end_t = excel_datetime_to_dt(workbook.datemode, lab_date, end_t_excel)
    return start_t.timestamp(), end_t.timestamp()


def matlab_datenum_to_dt(matlab_datenum):
    py_dt = datetime.fromordinal(int(matlab_datenum) - 366) + timedelta(days=matlab_datenum % 1)
    #print(py_dt)
    return py_dt

def unix_to_dt(unix_time):
    py_dt = datetime.fromtimestamp(unix_time)
    #print(py_dt)
    return py_dt

def excel_datetime_to_dt(excel_datemode, excel_date, excel_time):
    py_dt = datetime(*xlrd.xldate_as_tuple(excel_date.value + excel_time.value, excel_datemode))
    #print(py_dt)
    return py_dt

def dt_to_unix(py_dt):
    unix_time = py_dt.timestamp()
    return unix_time


if __name__ == '__main__':
    #subj = 'LWP2_0019'
    #read_task_timing_all(subj)
    print(unix_to_dt(1479236614.0))

    #get_lab_start_end_time(subj)
