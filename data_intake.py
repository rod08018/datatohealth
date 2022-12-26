import re
import os
import pandas as pd
from dotenv import load_dotenv
import database as db
import samsung
load_dotenv()


def preprocess_fitbit_files():
    pass


def preprocess_samsung_files(csv_list):
    curated_csv_list = []
    for csv in csv_list:
        csv_curated = re.sub(r'[0-9]+', '', csv)
        csv_curated = csv_curated.replace("com.samsung.shealth.", "")
        csv_curated = csv_curated.replace("com.samsung.health.", "")
        csv_curated = csv_curated.replace(".csv", "")
        csv_curated = csv_curated.replace(".", "_")
        csv_curated = csv_curated.strip('_')
        accepted_csvs = [
            'tracker_pedometer_step_count', 'sleep_combined', 'sleep_stage', 'activity_day_summary',
            'calories_burned_details', 'exercise', 'weight', 'preferences', 'sleep', 'step_daily_trend', 'stress',
            'stress_histogram', 'tracker_heart_rate', 'tracker_oxygen_saturation', 'tracker.pedometer_day_summary',
            'tracker_pedometer_step_count', 'nutrition', 'food_info', 'food_intake']
        if csv_curated in accepted_csvs:
            curated_csv_list.append(csv_curated)
            os.rename(
                os.path.join(os.path.join('datasets', 'downloaded_data/samsung'), csv),
                os.path.join(os.path.join('datasets', 'downloaded_data/samsung'), csv_curated) + ".csv"
            )
        else:
            os.remove(os.path.join(os.path.join('datasets', 'downloaded_data/samsung'), csv))

    return curated_csv_list


def clean_folder(path):
    csv_list = os.listdir(
        path
    )

    for file in csv_list:
        os.remove(os.path.join(path, file))


def get_watch_data():
    csv_list = preprocess_samsung_files(
        os.listdir(
            os.path.join('datasets', 'downloaded_data/samsung')
        )
    )
    watch_data_dict = {}
    for csv in csv_list:

        data = pd.read_csv(
            os.path.join(
                os.path.join('datasets', 'downloaded_data/samsung'), csv + '.csv'
            ),
            index_col=False,
            delimiter=',',
            skiprows=1
        )

        approved_att_list = [
            column.replace('com.samsung.shealth.', '').replace('com.samsung.health.', '')
            for column in data.columns if column not in [
                                 "goal",
                                 "others_time",
                                 "",
                                 "exercise.pkg_name",
                                 "exercise.exercise_custom_type",
                                 "exercise.datauuid",
                                 "exercise.sweat_loss",
                                 "exercise.pkg_name",
                                 "exercise.live_data",
                                 "exercise.comment",
                                 "exercise.deviceuuid",
                                 "exercise.additional",
                                 "exercise.location_data",
                                 "additional_internal",
                                 "location_data_internal",
                                 "heart_rate_deviceuuid",
                                 "program_schedule_id",
                                 "mission_extra_value",
                                 "mission_type",
                                 "tracking_status",
                                 "program_id",
                                 "title",
                                 "pace_live_data",
                                 "pace_info_id",
                                 "completion_status",
                                 "subset_data",
                                 "mission_value",
                                 "sleep_id",
                                 "create_time",
                                 "update_time",
                                 "algorithm",
                                 "comment",
                                 "original_efficiency",
                "original_bed_time",
                "",
                "",
                                 "heart_rate.comment",
                                 "heart_rate.pkg_name",
                                 "heart_rate.time_offset",
                                 "heart_rate.datauuid",
                                 "heart_rate.update_time",
                                 "heart_rate.create_time",
                                 "heart_rate.binning_data",
                                 "heart_rate.custom",
                                 "heart_rate.heart_beat_count",
                                 "oxygen_saturation.custom",
                                 "oxygen_saturation.create_time",
                                 "oxygen_saturation.update_time",
                                 "oxygen_saturation.binning",
                                 "oxygen_saturation.time_offset",
                                 "oxygen_saturation.deviceuuid",
                                 "oxygen_saturation.comment",
                                 "oxygen_saturation.pkg_name",
                                 "oxygen_saturation.datauuid",
                                 "version_code",
                                 "step_count.update_time",
                                 "step_count.create_time",
                                 "step_count.time_offset",
                                 "vfa_level",
                                 "comment",
                                 "time_offset",
                                 "muscle_mass",
                                 "heart_rate.deviceuuid",
                                 "heart_rate.comment",
                                 "heart_rate.pkg_name",
                                 "heart_rate.datauuid",
                                 "custom",
                                 "deviceuuid",
                                 "pkg_name",
                                 "datauuid",
                                 "extra_data",
                                 "device_type",
                                 "source",
                                 "source_id",
                                 "source_pkg_name",
                                 "com.samsung.shealth.calories_burned.pkg_name",
                                 "com.samsung.shealth.calories_burned.datauuid",
                                 "com.samsung.shealth.calories_burned.deviceuuid",
                                 "com.samsung.shealth.calories_burned.deviceuuid",
                                 "com.samsung.health.sleep.datauuid",
                                 "com.samsung.health.sleep.pkg_name",
                                 "com.samsung.health.sleep.deviceuuid",
                                 "com.samsung.health.sleep.comment",
                                 "binning_data",
                                 "tag_id",
                                 "source_type",
                                 "com.samsung.health.step_count.datauuid",
                                 "com.samsung.health.step_count.pkg_name",
                                 "com.samsung.health.step_count.deviceuuid",
                                 "com.samsung.health.step_count.sample_position_type",
                                 "com.samsung.health.step_count.custom",
                             ]
                             ]
        data.columns = data.columns.str.replace('com.samsung.shealth.', '', regex=False)
        data.columns = data.columns.str.replace('com.samsung.health.', '', regex=False)
        for column in data.columns:
            if "start_time" in column or "end_time" in column:
                data[column] = pd.to_datetime(data[column])
            elif "day_time" in column:
                data[column] = pd.to_datetime(data[column], unit='ms')
            elif "active" in column:
                data[column] = data[column] / 1000 / 60
        for column in data.columns:

            if "start_time" in column:
                data = data[(data[column] >= '11/14/2022')]
                break

        data['user_id'] = 1
        data.fillna(0, inplace=True)

        watch_data_dict[csv] = samsung.clean_table_data(data[approved_att_list], csv)
    clean_folder(os.path.join('datasets', 'downloaded_data/samsung'))
    return watch_data_dict


def body_scale_data(path, user):
    data = pd.read_csv(path, delimiter=',')
    data['user_id'] = user
    return data


def nutri_scale_data(path, user):
    data = pd.read_csv(path, delimiter=',')
    data['user_id'] = user
    return data


def tape_measure_data(path, user):
    data = pd.read_csv(path, delimiter=',')
    data['user_id'] = user
    return data


def get_user(file_name: str):
    return file_name.replace(".csv", "").split("-")[1]


def get_renpho_data():
    csv_list = os.listdir(os.path.join('datasets', 'digital_scale_data_dump'))
    renpho_data = {}
    renpho_path = os.path.join('datasets', 'renpho')
    for csv in csv_list:
        user = get_user(csv)
        if "Body Scale" in csv:
            renpho_data['body_scale'] = body_scale_data(
                os.path.join(renpho_path, csv),
                user
            )
        elif "Nutri" in csv:
            renpho_data['nutri_scale'] = nutri_scale_data(
                os.path.join(renpho_path, csv),
                user
            )
        elif "Tape" in csv:
            renpho_data['tape_measure'] = tape_measure_data(
                os.path.join(renpho_path, csv),
                user
            )
    clean_folder(
        renpho_path
    )
    return renpho_data


def get_data(path):
    if "samsung" in path:
        db.manage_db_watch_data(get_watch_data())
    elif "renpho" in path:
        get_renpho_data()
    elif "fitbit" in path:
        # TODO: build fitbit intake()
        # get_fitbit_data()
        pass