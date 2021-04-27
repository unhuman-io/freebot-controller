#!/usr/bin/env python3

import subprocess
import create_table
import motor
import time

def collect_data(timeout=20):
    try:    
        f = open("infile", "w")
        subprocess.run(["motor_util", "read", "--csv"], timeout=timeout, stdout=f)
    except subprocess.TimeoutExpired:
        pass

def get_index_offset():
    m = motor.MotorManager()
    m.set_command_mode(motor.ModeDesired.Velocity) # make sure past index
    m.set_command_velocity([6])
    m.write_saved_commands()
    time.sleep(2)
    assert(m.motors()[0]["index_received"].get())
    m.set_command_current([5])
    m.set_command_mode(motor.ModeDesired.PhaseLock)
    m.write_saved_commands()
    time.sleep(2)
    phase_lock = m.read()[0].motor_encoder 
    index_pos = int(m.motors()[0]["index_pos"].get())
    index_electrical_offset_pos = phase_lock - index_pos
    print("index_electrical_offset_pos = motor_encoder - index_pos = {} - {} = {}".format(
        phase_lock, index_pos, index_electrical_offset_pos))
    print("mod = {}".format(index_electrical_offset_pos % (8192/10)))
    m.set_command_mode(motor.ModeDesired.Open)
    m.write_saved_commands()

def make_cogging_table():
    m = motor.MotorManager()
    m.set_command_position_tuning(motor.TuningMode.Triangle, 6, .1, 0)
    m.write_saved_commands()
    time.sleep(1)
    collect_data()
    create_table.Table(["infile", "../calibration/freebot_g474/motor_enc_small_j4/cog.dat", "-c", "8192", "-i", m.motors()[0]["index_pos"].get()])
    m.set_command_mode(motor.ModeDesired.Open)
    m.write_saved_commands()

def make_encoder_table():
    m = motor.MotorManager()
    m.set_command_stepper_velocity(2, 30)
    m.write_saved_commands()
    time.sleep(1)
    collect_data()
    create_table.Table(["infile", "../calibration/freebot_g474/motor_enc_small_j4/enc.dat", "-c", "8192", "-i", m.motors()[0]["index_pos"].get(), "-e"])
    m.set_command_mode(motor.ModeDesired.Open)
    m.write_saved_commands()

if __name__ == "__main__":
    get_index_offset()
    make_cogging_table()
    make_encoder_table()