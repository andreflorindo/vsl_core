# coding=utf-8

import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import re


class CourseClass:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class JointStates:
    def __init__(self):
        self.a1 = []
        self.a2 = []
        self.a3 = []
        self.a4 = []
        self.a5 = []
        self.a6 = []


class EEStates:
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        self.a = []
        self.b = []
        self.c = []


class RobotState:
    def __init__(self):
        self.time = []
        self.joint_request = JointStates()
        self.joint_states = JointStates()
        self.ee_request = EEStates()
        self.ee_states = EEStates()


class EEVelocity:
    def __init__(self):
        self.time = []
        self.linear_velocity = []
        self.angular_velocity = []


def read_path(robot_state_from_file):
    i = 0
    infile = open(
        # '/home/andreflorindo/workspaces/vsl_motion_planner_ws/src/vsl_core/trial_txt_files/14_11_2019/10_angle_spline_rsi.txt', 'r')
        '/home/andreflorindo/workspaces/vsl_motion_planner_ws/src/vsl_core/trial_txt_files/03_12_2019/rsi_const_laydown_speed.txt', 'r')
    # '/home/andre/workspaces/vsl_msc_project_ws/src/vsl_core/trial_txt_files/rsi_xml_doc_01_11.txt', 'r')
    for line in infile:
        input = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        if len(input) != 0:
            robot_state_from_file.time.append(i*0.004)
            robot_state_from_file.ee_states.x.append(float(input[1])*0.001)
            robot_state_from_file.ee_states.y.append(float(input[2])*0.001)
            robot_state_from_file.ee_states.z.append(float(input[3])*0.001)
            robot_state_from_file.ee_states.a.append(float(input[4])*np.pi/180)
            robot_state_from_file.ee_states.b.append(float(input[5])*np.pi/180)
            robot_state_from_file.ee_states.c.append(float(input[6])*np.pi/180)
            # robot_state_from_file.ee_request.x.append(float(input[7])*0.001)
            # robot_state_from_file.ee_request.y.append(float(input[8])*0.001)
            # robot_state_from_file.ee_request.z.append(float(input[9])*0.001)
            # robot_state_from_file.ee_request.a.append(
            #     float(input[10])*np.pi/180)
            # robot_state_from_file.ee_request.b.append(
            #     float(input[11])*np.pi/180)
            # robot_state_from_file.ee_request.c.append(
            #     float(input[12])*np.pi/180)
            robot_state_from_file.joint_states.a1.append(
                float(input[14])*np.pi/180)
            robot_state_from_file.joint_states.a2.append(
                float(input[16])*np.pi/180)
            robot_state_from_file.joint_states.a3.append(
                float(input[18])*np.pi/180)
            robot_state_from_file.joint_states.a4.append(
                float(input[20])*np.pi/180)
            robot_state_from_file.joint_states.a5.append(
                float(input[22])*np.pi/180)
            robot_state_from_file.joint_states.a6.append(
                float(input[24])*np.pi/180)
            # robot_state_from_file.joint_request.a1.append(
            #     float(input[26])*np.pi/180)
            # robot_state_from_file.joint_request.a2.append(
            #     float(input[28])*np.pi/180)
            # robot_state_from_file.joint_request.a3.append(
            #     float(input[30])*np.pi/180)
            # robot_state_from_file.joint_request.a4.append(
            #     float(input[32])*np.pi/180)
            # robot_state_from_file.joint_request.a5.append(
            #     float(input[34])*np.pi/180)
            # robot_state_from_file.joint_request.a6.append(
            #     float(input[36])*np.pi/180)
            i = i+1
    infile.close()


def clean_path(robot_state_from_file, robot_state):
    j = 0
    for i in range(1, len(robot_state_from_file.time)):
        if robot_state_from_file.joint_states.a1[i] != robot_state_from_file.joint_states.a1[i-1] or j != 0:
            robot_state.time.append(0.004*j)
            # robot_state.joint_request.a1.append(
            #     robot_state_from_file.joint_request.a1[i])
            # robot_state.joint_request.a2.append(
            #     robot_state_from_file.joint_request.a2[i])
            # robot_state.joint_request.a3.append(
            #     robot_state_from_file.joint_request.a3[i])
            # robot_state.joint_request.a4.append(
            #     robot_state_from_file.joint_request.a4[i])
            # robot_state.joint_request.a5.append(
            #     robot_state_from_file.joint_request.a5[i])
            # robot_state.joint_request.a6.append(
            #     robot_state_from_file.joint_request.a6[i])
            robot_state.joint_states.a1.append(
                robot_state_from_file.joint_states.a1[i])
            robot_state.joint_states.a2.append(
                robot_state_from_file.joint_states.a2[i])
            robot_state.joint_states.a3.append(
                robot_state_from_file.joint_states.a3[i])
            robot_state.joint_states.a4.append(
                robot_state_from_file.joint_states.a4[i])
            robot_state.joint_states.a5.append(
                robot_state_from_file.joint_states.a5[i])
            robot_state.joint_states.a6.append(
                robot_state_from_file.joint_states.a6[i])
            robot_state.ee_states.x.append(
                robot_state_from_file.ee_states.x[i])
            robot_state.ee_states.y.append(
                robot_state_from_file.ee_states.y[i])
            robot_state.ee_states.z.append(
                robot_state_from_file.ee_states.z[i])
            robot_state.ee_states.a.append(
                robot_state_from_file.ee_states.a[i])
            robot_state.ee_states.b.append(
                robot_state_from_file.ee_states.b[i])
            robot_state.ee_states.c.append(
                robot_state_from_file.ee_states.c[i])
            # robot_state.ee_request.x.append(
            #     robot_state_from_file.ee_request.x[i])
            # robot_state.ee_request.y.append(
            #     robot_state_from_file.ee_request.y[i])
            # robot_state.ee_request.z.append(
            #     robot_state_from_file.ee_request.z[i])
            # robot_state.ee_request.a.append(
            #     robot_state_from_file.ee_request.a[i])
            # robot_state.ee_request.b.append(
            #     robot_state_from_file.ee_request.b[i])
            # robot_state.ee_request.c.append(
            #     robot_state_from_file.ee_request.c[i])
            j = j+1


def compute_derivative(time, variable):
    v = []

    #  Finite difference, first order, central.
    v.append(0)
    for i in range(1, len(time)-1):
        delta_theta = variable[i + 1] - variable[i - 1]
        delta_time = time[i + 1] - time[i - 1]
        v.append(delta_theta / delta_time)
    v.append(0)

    #   Finite difference, first order, forward difference
    # for i in range(0, len(time)-1):
    #     delta_theta = variable[i + 1] - variable[i]
    #     delta_time = time[i + 1] - time[i]
    #     v.append(delta_theta / delta_time)
    # v.append(0)

    #   Finite difference, first order, backward difference
    # v.append(0)
    # for i in range(1, len(time)):
    #     delta_theta = variable[i] - variable[i-1]
    #     delta_time = time[i] - time[i-1]
    #     v.append(delta_theta / delta_time)

    #   Finite difference, second order, forward difference
    # for i in range(0, len(time)-2):
    #     delta_theta = -variable[i + 2] + 4*variable[i+1] -3*variable[i]
    #     delta_time = time[i + 2] - time[i]
    #     v.append(delta_theta / delta_time)
    # v.append(0)
    # v.append(0)

    #   Finite difference, second order, backward difference
    # v.append(0)
    # v.append(0)
    # for i in range(2, len(time)):
    #     delta_theta = 3*variable[i] - 4*variable[i-1] - variable[i-2]
    #     delta_time = time[i] - time[i-2]
    #     v.append(delta_theta / delta_time)

    return v


def fill_derivative_class(robot_state, robot_state_velocity):
    robot_state_velocity.time = robot_state.time

    # # Joint request Velocity
    # robot_state_velocity.joint_request.a1 = compute_derivative(
    #     robot_state.time, robot_state.joint_request.a1)
    # robot_state_velocity.joint_request.a2 = compute_derivative(
    #     robot_state.time, robot_state.joint_request.a2)
    # robot_state_velocity.joint_request.a3 = compute_derivative(
    #     robot_state.time, robot_state.joint_request.a3)
    # robot_state_velocity.joint_request.a4 = compute_derivative(
    #     robot_state.time, robot_state.joint_request.a4)
    # robot_state_velocity.joint_request.a5 = compute_derivative(
    #     robot_state.time, robot_state.joint_request.a5)
    # robot_state_velocity.joint_request.a6 = compute_derivative(
    #     robot_state.time, robot_state.joint_request.a6)

    # Joint States velocity
    robot_state_velocity.joint_states.a1 = compute_derivative(
        robot_state.time, robot_state.joint_states.a1)
    robot_state_velocity.joint_states.a2 = compute_derivative(
        robot_state.time, robot_state.joint_states.a2)
    robot_state_velocity.joint_states.a3 = compute_derivative(
        robot_state.time, robot_state.joint_states.a3)
    robot_state_velocity.joint_states.a4 = compute_derivative(
        robot_state.time, robot_state.joint_states.a4)
    robot_state_velocity.joint_states.a5 = compute_derivative(
        robot_state.time, robot_state.joint_states.a5)
    robot_state_velocity.joint_states.a6 = compute_derivative(
        robot_state.time, robot_state.joint_states.a6)

    # EE States Velocity
    robot_state_velocity.ee_states.x = compute_derivative(
        robot_state.time, robot_state.ee_states.x)
    robot_state_velocity.ee_states.y = compute_derivative(
        robot_state.time, robot_state.ee_states.y)
    robot_state_velocity.ee_states.z = compute_derivative(
        robot_state.time, robot_state.ee_states.z)
    robot_state_velocity.ee_states.a = compute_derivative(
        robot_state.time, robot_state.ee_states.a)
    robot_state_velocity.ee_states.b = compute_derivative(
        robot_state.time, robot_state.ee_states.b)
    robot_state_velocity.ee_states.c = compute_derivative(
        robot_state.time, robot_state.ee_states.c)

    # EE Request Velocity
    # robot_state_velocity.ee_states.x = compute_derivative(
    #     robot_state.time, robot_state.ee_request.x)
    # robot_state_velocity.ee_states.y = compute_derivative(
    #     robot_state.time, robot_state.ee_request.y)
    # robot_state_velocity.ee_states.z = compute_derivative(
    #     robot_state.time, robot_state.ee_request.z)
    # robot_state_velocity.ee_states.a = compute_derivative(
    #     robot_state.time, robot_state.ee_request.a)
    # robot_state_velocity.ee_states.b = compute_derivative(
    #     robot_state.time, robot_state.ee_request.b)
    # robot_state_velocity.ee_states.c = compute_derivative(
    #     robot_state.time, robot_state.ee_request.c)


def compute_ee_velocity(robot_state_velocity, ee_velocity):
    ee_velocity.time = robot_state_velocity.time
    for i in range(0, len(robot_state_velocity.time)):
        ee_velocity.linear_velocity.append(math.sqrt(robot_state_velocity.ee_states.x[i]**2 +
                                                     robot_state_velocity.ee_states.y[i]**2+robot_state_velocity.ee_states.z[i]**2))
        ee_velocity.angular_velocity.append(math.sqrt(robot_state_velocity.ee_states.a[i]**2 +
                                                      robot_state_velocity.ee_states.b[i]**2+robot_state_velocity.ee_states.c[i]**2))

    return ee_velocity


def plot_joint_state(robot_state, robot_state_velocity, robot_state_acceleration):
    plt.figure()

    plt.subplot(311)
    plt.title('Joint State A1')
    plt.ylabel('Angle(rad)')
    plt.plot(robot_state.time, robot_state.joint_states.a1)

    plt.subplot(312)
    plt.ylabel('Speed(rad/s)')
    plt.plot(robot_state_velocity.time, robot_state_velocity.joint_states.a1)

    plt.subplot(313)
    plt.ylabel('Acceleration(rad/s^2)')
    plt.xlabel('Time (s)')
    plt.plot(robot_state_acceleration.time,
             robot_state_acceleration.joint_states.a1)
    plt.show()

    plt.figure()

    plt.subplot(311)
    plt.title('Joint State A2')
    plt.ylabel('Angle(rad)')
    plt.plot(robot_state.time, robot_state.joint_states.a2)

    plt.subplot(312)
    plt.ylabel('Speed(rad/s)')
    plt.plot(robot_state_velocity.time, robot_state_velocity.joint_states.a2)

    plt.subplot(313)
    plt.ylabel('Acceleration(rad/s^2)')
    plt.xlabel('Time (s)')
    plt.plot(robot_state_acceleration.time,
             robot_state_acceleration.joint_states.a2)
    plt.show()

    plt.figure()

    plt.subplot(311)
    plt.title('Joint State A3')
    plt.ylabel('Angle(rad)')
    plt.plot(robot_state.time, robot_state.joint_states.a3)

    plt.subplot(312)
    plt.ylabel('Speed(rad/s)')
    plt.plot(robot_state_velocity.time, robot_state_velocity.joint_states.a3)

    plt.subplot(313)
    plt.ylabel('Acceleration(rad/s^2)')
    plt.xlabel('Time (s)')
    plt.plot(robot_state_acceleration.time,
             robot_state_acceleration.joint_states.a3)
    plt.show()

    plt.figure()

    plt.subplot(311)
    plt.title('Joint State A4')
    plt.ylabel('Angle(rad)')
    plt.plot(robot_state.time, robot_state.joint_states.a4)

    plt.subplot(312)
    plt.ylabel('Speed(rad/s)')
    plt.plot(robot_state_velocity.time, robot_state_velocity.joint_states.a4)

    plt.subplot(313)
    plt.ylabel('Acceleration(rad/s^2)')
    plt.xlabel('Time (s)')
    plt.plot(robot_state_acceleration.time,
             robot_state_acceleration.joint_states.a4)
    plt.show()

    plt.figure()

    plt.subplot(311)
    plt.title('Joint State A5')
    plt.ylabel('Angle(rad)')
    plt.plot(robot_state.time, robot_state.joint_states.a5)

    plt.subplot(312)
    plt.ylabel('Speed(rad/s)')
    plt.plot(robot_state_velocity.time, robot_state_velocity.joint_states.a5)

    plt.subplot(313)
    plt.ylabel('Acceleration(rad/s^2)')
    plt.xlabel('Time (s)')
    plt.plot(robot_state_acceleration.time,
             robot_state_acceleration.joint_states.a5)
    plt.show()

    plt.figure()

    plt.subplot(311)
    plt.title('Joint State A6')
    plt.ylabel('Angle(rad)')
    plt.plot(robot_state.time, robot_state.joint_states.a6)

    plt.subplot(312)
    plt.ylabel('Speed(rad/s)')
    plt.plot(robot_state_velocity.time, robot_state_velocity.joint_states.a6)

    plt.subplot(313)
    plt.ylabel('Acceleration(rad/s^2)')
    plt.xlabel('Time (s)')
    plt.plot(robot_state_acceleration.time,
             robot_state_acceleration.joint_states.a6)
    plt.show()


def plot_ee_state(robot_state, ee_velocity):
    plt.figure()

    plt.subplot(411)
    plt.ylabel('Distance x (m)')
    plt.plot(robot_state.time, robot_state.ee_states.x)

    plt.subplot(412)
    plt.ylabel('Distance y (m)')
    plt.plot(robot_state.time, robot_state.ee_states.y)

    plt.subplot(413)
    plt.ylabel('Distance z (m)')
    plt.plot(robot_state.time, robot_state.ee_states.z)

    plt.subplot(414)
    plt.ylabel('Laydown Speed (m/s)')
    plt.xlabel('Time (s)')
    plt.plot(ee_velocity.time, ee_velocity.linear_velocity)
    plt.show()

    plt.figure()

    plt.subplot(411)
    plt.ylabel('Angle A (rad)')
    plt.plot(robot_state.time, robot_state.ee_states.a)

    plt.subplot(412)
    plt.ylabel('Angle B (rad)')
    plt.plot(robot_state.time, robot_state.ee_states.b)

    plt.subplot(413)
    plt.ylabel('Angle C (rad)')
    plt.plot(robot_state.time, robot_state.ee_states.c)

    plt.subplot(414)
    plt.ylabel('Angular Speed(rad/s)')
    plt.xlabel('Time (s)')
    plt.plot(ee_velocity.time, ee_velocity.angular_velocity)
    plt.show()

    plt.figure()

# def find_switch_point(robot_state_velocity):
#     index_switch = []
#     index_switch.append(0)
#     path_started = True
#     for i in range(1, len(robot_state_velocity .time)-2):
#         if robot_state_velocity.joint_states.a1[i-1] == 0 and path_started == False:
#             if robot_state_velocity.joint_states.a1[i] == 0:
#                 if robot_state_velocity.joint_states.a1[i+1] != 0:
#                     if robot_state_velocity.joint_states.a1[i+2] != 0 and abs(robot_state_velocity.joint_states.a1[i+2]) > 0.0008:
#                         index_switch.append(i)
#                         path_started = True

#         if robot_state_velocity.joint_states.a1[i-1] != 0 and path_started == True:
#             if robot_state_velocity.joint_states.a1[i] == 0:
#                 if robot_state_velocity.joint_states.a1[i+1] == 0:
#                     index_switch.append(i)
#                     path_started = False
#     return index_switch


def find_switch_point(robot_state_velocity):
    index_switch = []
    index_switch.append(0)
    j = 0
    path_started = True
    for i in range(1, len(robot_state_velocity .time)-1):
        if abs(robot_state_velocity.joint_states.a1[i-1]) < 0.0003 and i-index_switch[j] > 10 and path_started == False:
            if abs(robot_state_velocity.joint_states.a1[i]) < 0.0003:
                if abs(robot_state_velocity.joint_states.a1[i+1]) > 0.0003:
                    index_switch.append(i)
                    j = j+1
                    path_started = True

        if abs(robot_state_velocity.joint_states.a1[i-1]) > 0.0003 and i-index_switch[j] > 10 and path_started == True:
            if abs(robot_state_velocity.joint_states.a1[i]) < 0.0003:
                if abs(robot_state_velocity.joint_states.a1[i+1]) < 0.0003:
                    index_switch.append(i)
                    j = j+1
                    path_started = False
    return index_switch


def read_course_path():
    input = np.loadtxt(
        "/home/andreflorindo/workspaces/vsl_motion_planner_ws/src/vsl_core/examples/simplePath.txt", dtype='f')
    x = []
    y = []
    z = []
    for i in range(0, len(input)):
        x.append(input[i][0])
        y.append(input[i][1])
        z.append(input[i][2])

    course = CourseClass(x, y, z)
    return course


def plot_path(robot_state, index_switch):
    x = []
    y = []

    course = read_course_path()

    # Rotate ee_state by -90 degrees and make sure that it starts at same spot as the given course
    for i in range(index_switch[4], len(robot_state.ee_states.y)):
        # for i in range(index_switch[4], index_switch[5]):
        # x=x_course0+(y_ee-y_ee0)
        x.append(course.x[0]+(robot_state.ee_states.y[i] -
                              robot_state.ee_states.y[index_switch[4]]))  # 250
        # y=y_course0+(-x_ee+x_ee0)
        y.append(course.y[0]+(-robot_state.ee_states.x[i] +
                              robot_state.ee_states.x[index_switch[4]]))  # 250

    plt.figure()
    plt.title('Path performed')
    plt.ylabel('y(m)')
    plt.xlabel('x(m)')
    plt.plot(course.x, course.y, 'r--.', label='Path requested')
    plt.plot(x, y, 'b', label='Path performed')
    plt.legend()
    plt.show()

    plt.figure()


if __name__ == "__main__":

    robot_state_from_file = RobotState()
    robot_state = RobotState()
    robot_state_velocity = RobotState()
    robot_state_acceleration = RobotState()
    ee_velocity = EEVelocity()
    index_switch = []

    read_path(robot_state_from_file)

    clean_path(robot_state_from_file, robot_state)

    fill_derivative_class(robot_state, robot_state_velocity)
    fill_derivative_class(robot_state_velocity, robot_state_acceleration)
    compute_ee_velocity(robot_state_velocity, ee_velocity)

    index_switch = find_switch_point(robot_state_velocity)

    # plot_joint_state(robot_state, robot_state_velocity,
    #                  robot_state_acceleration)
    # plot_ee_state(robot_state, ee_velocity)

    print(index_switch)
    plot_path(robot_state, index_switch)
