/* Author: Andre Florindo*/

#include <ee_velocity_publisher.h>

namespace vsl_motion_planning
{

CartesianVelocityPublisher::CartesianVelocityPublisher() {}
CartesianVelocityPublisher::~CartesianVelocityPublisher() {}

void CartesianVelocityPublisher::initTopic()
{
    ros::NodeHandle nh;
    ros::NodeHandle ph("~");

    if (ph.getParam("tip_link", config_.tip_link) &&
        ph.getParam("base_link", config_.base_link))
    {
        ROS_INFO_STREAM("ee_velocity_publisher: Loaded Topic parameters");
    }
    else
    {
        ROS_ERROR_STREAM("ee_velocity_publisher: Failed to load Topic parameters");
        exit(-1);
    }

    joint_path_subscriber_ = nh.subscribe("joint_path_command", 1000, &CartesianVelocityPublisher::subscriberCallback, this);

    joint_request_publisher_ = nh.advertise<vsl_core::JointRequest>("joint_request", 1000, true);

    ROS_INFO_STREAM("ee_velocity_publisher: Task '" << __FUNCTION__ << "' completed");
}

void CartesianVelocityPublisher::subscriberCallback(const trajectory_msgs::JointTrajectory &msg)
{
    seq++;
    time_point = ros::Time::now();
    joint_path_ = msg;
    ROS_INFO("ee_velocity_publisher: Joint trajectory %d received", seq);
    publishJointRequest();
}

void CartesianVelocityPublisher::publishJointRequest()
{
    std::vector<std::vector<double>> buffer_position;
    std::vector<std::vector<double>> buffer_velocity;
    std::vector<std::vector<double>> buffer_acceleration;
    std::vector<std::vector<double>> buffer_jerk;
    std::vector<double> buffer_time;
    
    vsl_core::JointRequest joint_request;

    int num_joints = joint_path_.points[0].positions.size();
    int num_points = joint_path_.points.size();

    buffer_position.resize(num_points, std::vector<double>(num_joints));
    buffer_velocity.resize(num_points, std::vector<double>(num_joints));
    buffer_acceleration.resize(num_points, std::vector<double>(num_joints));
    buffer_jerk.resize(num_points, std::vector<double>(num_joints));
    buffer_time.resize(num_points - 1);

    for (int j = 0; j < num_points - 1; j++)
    {
        buffer_time[j] = joint_path_.points[j + 1].time_from_start.toSec() - joint_path_.points[j].time_from_start.toSec();
    }

    for (int j = 0; j < num_points; j++)
    {
        for (int i = 0; i < num_joints; i++)
        {
            buffer_position[j][i] = joint_path_.points[j].positions[i];
            buffer_velocity[j][i] = joint_path_.points[j].velocities[i];
            buffer_acceleration[j][i] = joint_path_.points[j].accelerations[i];
            buffer_jerk[j][i] = 0.0f;
        }
    }

    for (int j = 0; j < num_points; j++)
    {
        if (j != 0)
            time_point = joint_request.header.stamp + ros::Duration(buffer_time[j - 1]);

        joint_request.header.seq = total_num_points;
        joint_request.header.stamp = time_point;
        joint_request.name = joint_path_.joint_names;
        joint_request.position = buffer_position[j];
        joint_request.velocity = buffer_velocity[j];
        joint_request.acceleration = buffer_acceleration[j];
        joint_request.jerk = buffer_jerk[j];

        joint_request_publisher_.publish(joint_request);
        total_num_points++;
    }

    ROS_INFO_STREAM("ee_velocity_publisher: Task '" << __FUNCTION__ << "' completed");
}

} // namespace vsl_motion_planning

int main(int argc, char **argv)
{
    ros::init(argc, argv, "ee_velocity_publisher");

    vsl_motion_planning::CartesianVelocityPublisher ee_velocity_publisher;

    ee_velocity_publisher.initTopic();

    ros::spin();
}